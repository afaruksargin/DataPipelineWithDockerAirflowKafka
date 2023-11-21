import psycopg2
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import json

def delivery_report(err, msg):
    if err is not None:
        print(f'Hata oluştu: {err}')
    else:
        print(f'Mesaj başarıyla gönderildi: {msg.topic()}[{msg.partition()}] at offset {msg.offset()}')


def produce_from_db_to_kafka(topic_name, db_config):
    #Veri Tabanı Bağlantısı Oluşturma
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

    except psycopg2.Error as e:
        print(f"Veri Tabanı Bağlantı Hatası {e}")
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    # AdminClient oluştur
    admin_client = AdminClient({'bootstrap.servers': '172.18.0.3:9092'})
    # Konuyu oluştur
    new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
    admin_client.create_topics([new_topic])


    # Kafka Producer Konfigürasyonu
    producer_conf = {
        'bootstrap.servers':'172.18.0.3:9092',
        'client.id': 'produce_from_db_to_kafka'
    }

    producer = Producer(producer_conf)

    try:
        cursor.execute("SELECT * FROM staging.example")
        rows = cursor.fetchall()

        for row in rows:
            #Her Bir Satırdaki Verileri Kafka Topice Gönder
            data_json = json.dumps(row) 
            producer.produce(topic_name  , key=None, value=data_json , callback = delivery_report)
        producer.flush()

    except Exception as e:
        print(f'Hata oluştu: {e}')
    finally:
        # Bağlantıları kapatma
        if 'conn' in locals():
            conn.close()
        # Producer'ı kapatma
        producer.flush()

def main():
    # Kullanımı
    kafka_topic = 'public'  # Kafka'daki topic adı
    db_connection_config = {
        'host': 'localhost',
        'user': 'postgres',
        'password': '1234',
        'dbname': 'postgres'
    }

    produce_from_db_to_kafka(kafka_topic, db_connection_config)

if __name__ ==  '__main__':
    main()