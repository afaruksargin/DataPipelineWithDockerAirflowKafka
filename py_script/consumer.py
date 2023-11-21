import socket
from confluent_kafka import Consumer
import json
import pandas as pd
from io import StringIO
import os
import sys
import psycopg2
from psycopg2 import sql

conf = {'bootstrap.servers':'172.18.0.3:9092',
        'group.id':"topic-to-staging"}

consumer1 = Consumer(conf)

def consumer_func(consumer,topics,max_messages=17000):
    data = []
    message_count = 0
    try:
        consumer.subscribe(topics)

        while message_count < max_messages:
            msg = consumer.poll(timeout =1.0)
            if msg is None : continue
            if msg.error():
                print("hata var")
            else:
                json_data = msg.value().decode('utf-8')

                python_dict = json.loads(json_data)

                data.append(python_dict)

                message_count += 1
    except Exception as e:
        # Hata oluştuğunda ne yapılacağını belirleyebilirsiniz.
        print(f'Hata oluştu: {e}')
        return None            
    finally:
        dataframe = pd.DataFrame(data)
        consumer.close()
        return dataframe


cr_table_sql_script = (f"CREATE TABLE IF NOT EXISTS staging.example" +
                    "(Country varchar(200) NULL , Month varchar(50) NULL , Year int NULL, Visitor float NULL);")


def write_dataframe_to_postgres(dataframe, schema_name='staging', table_name='example'):

    try:
        # Veritabanına bağlan
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="1234",
            database="postgres"
        )

        # DataFrame'i CSV formatına dönüştür
        csv_data = dataframe.to_csv(index=False, header=False)

        # CSV formatındaki veriyi bir bellek tamponuna yaz
        csv_buffer = StringIO()
        csv_buffer.write(csv_data)
        csv_buffer.seek(0)

        # Cursor oluştur
        cursor = connection.cursor()
        cursor.execute(cr_table_sql_script)

        # CSV verisini PostgreSQL tablosuna kopyala
        copy_query = sql.SQL("COPY {}.{} FROM STDIN WITH CSV").format(
            sql.Identifier(schema_name),
            sql.Identifier(table_name)
        )
        cursor.copy_expert(sql=copy_query, file=csv_buffer)
        connection.commit()
        print("DataFrame başarılı bir şekilde veritabanına aktarıldı.")

    except psycopg2.Error as e:
        print(f"PSQL Hatası: {e}")

    finally:
        # Bağlantıyı kapat
        if 'connection' in locals():
            connection.close()

def main():
    try :
        dataframe = consumer_func(consumer=consumer1,topics=["staging"],max_messages=17000)
        if dataframe is not None:
            # BURADA DATAFRAME ÜZERİNDE İŞLEMELER GERÇEKLEŞEBİLİR.
            print(dataframe.head())
            write_dataframe_to_postgres(dataframe)
        else:
            print("Topicten Veri alınırken bir hata oluştu")
    except Exception as e:
        print(f"Bir Hata Alınıdnı {e}")
    finally:
        # Consumerı Kapatma İşlemi
        if consumer1 is not None:
            consumer1.close()

if __name__ ==  '__main__':
    main()