from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import pandas as pd

def produce_to_kafka(topic, brokers, dataframe):
    def delivery_report(err, msg):
        if err is not None:
            print("Hatalı gönderme oldu {} {}".format(str(msg), str(err)))
        else:
            print('Başarılı Gönderme: {}'.format(str(msg)))

    try:
        # AdminClient oluştur
        admin_client = AdminClient({'bootstrap.servers': brokers})

        # Konuyu oluştur
        new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)
        admin_client.create_topics([new_topic])

        # Kafka producer oluşturma
        producer = Producer({
            'bootstrap.servers': brokers,
            'client.id': 'python-producer'
        })

        # Her bir satırı Kafka topic'ine yazma
        for _, row in dataframe.iterrows():
            producer.produce(topic, key=None, value=row.to_json(), callback=delivery_report)

        # Kafka'ya gönderilen mesajları bekletme
        producer.flush()

    except Exception as e:
        print(f"Bir hata oluştu: {e}")


def main():
    # Örnek DataFrame
    df = pd.read_csv("/home/user/Masaüstü/kafka/dataset/Number of foreign visitors to Japan by month_ .csv")

    # Kafka konfigürasyonları
    kafka_brokers = "172.18.0.3:9092"
    kafka_topic = "staging"

    # Kafka'ya DataFrame'i gönder
    produce_to_kafka(kafka_topic, kafka_brokers, df)

if __name__ ==  '__main__':
    main()