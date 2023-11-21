# Kafka-Airflow-Docker Projesi

Bu proje, Apache Kafka, Apache Airflow ve Docker kullanarak yapılan bir sistemdir. CSV dosyasından veri alınarak Kafka topic'ine yazılır, daha sonra Airflow ile bu veriler bir veritabanına aktarılır. Sonrasında yıllara göre veriler ayrıştırılır, belirli bir koşulu sağlayan veriler değiştirilip başka bir tabloya aktarılır.

## Gereksinimler

- [Docker](https://www.docker.com/)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache Airflow](https://airflow.apache.org/)
- Veritabanı (örneğin: PostgreSQL, MySQL)

## Kurulum

1. **Docker Kurulumu:** Docker'ı [resmi web sitesinden](https://www.docker.com/products/docker-desktop) indirip kurun.

2. **Kafka ve Zookeeper:** Docker üzerinde Kafka ve Zookeeper servislerini başlatmak için terminalde şu komutları çalıştırın:

    ```bash
    docker-compose up -d kafka zookeeper
    ```

3. **Apache Airflow:** Airflow'u Docker ile başlatmak için terminalde şu komutu çalıştırın:

    ```bash
    docker-compose up -d airflow
    ```

4. **Veritabanı:** Kendi tercihinize göre bir veritabanı oluşturun ve bağlantı yapılandırmalarını ayarlayın.

## Kullanım

1. CSV dosyasından verileri Kafka topic'ine yazmak için bir üretici (producer) yazılımı kullanın. Örnek komut:

    ```bash
    python kafka_producer.py --file data.csv --topic my_topic
    ```

2. Airflow arayüzünden DAG'ı çalıştırın. Bu DAG, Kafka'dan verileri çeker ve veritabanına yazar.

3. Veritabanında bulunan verileri işleyip yıllara göre ayrıştıran bir işleyici (processor) yazın ve belirli koşullara göre verileri değiştirip başka bir tabloya aktarın.

4. Örnek olarak:

    ```python
    # Yıl bazında verileri ayrıştırma ve işleme
    processed_data = process_data(raw_data)  # Verileri işleyin (ör. yıllara göre ayrıştırın)

    # Koşulu sağlayan verileri değiştirme
    processed_data = change_data_condition(processed_data)  # Örneğin, visitor < 1000 olanları değiştirin

    # Verileri başka bir tabloya aktarma
    write_to_another_table(processed_data)  # İşlenmiş verileri başka bir tabloya aktarın
    ```
