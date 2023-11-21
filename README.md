# Kafka-Airflow-Docker Projesi

Bu proje, Apache Kafka, Apache Airflow ve Docker kullanarak yapılan bir sistemdir. CSV dosyasından veri alınarak Kafka topic'ine yazılır, daha sonra Airflow ile bu veriler bir veritabanına aktarılır. Sonrasında yıllara göre veriler ayrıştırılır, belirli bir koşulu sağlayan veriler değiştirilip başka bir tabloya aktarılır.

![proje_akis drawio](https://github.com/afaruksargin/DataPipelineWithDockerAirflowKafka/assets/114520791/74263d27-2f8a-4dd5-a17e-ff1ebcbf5c61)


## Gereksinimler

- [Docker](https://www.docker.com/)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache Airflow](https://airflow.apache.org/)
- Veritabanı (örneğin: PostgreSQL)

## Kurulum

1. **Docker Kurulumu:** Docker'ı [resmi web sitesinden](https://www.docker.com/products/docker-desktop) indirip kurun.

2. **Kafka ve Zookeeper:** Docker üzerinde Kafka ve Zookeeper servislerini başlatmak için terminalde şu komutları çalıştırın:
    Network Ağı Oluşturma
    ```bash
    docker network create kafka-network --driver bridge
    ```
    İmage Kullanarak zookeper-kurma
    ```bash
    docker run -d --name zookeeper-server  --network kafka-network  -e ALLOW_ANONYMOUS_LOGIN=yes   bitnami/zookeeper:latest
    ```
    Image kullanarak kafka-server kurma
    ```bash
    docker run -d --name kafka-server   --network kafka-network -p 9090   -e ALLOW_PLAINTEXT_LISTENER=yes  -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper-server:2181   bitnami/kafka:latest
    ```
    Kafka Arayüzü Kurma Opsiyonel
    ```bash
    docker run -d --rm -p 9000:9000   --network kafka-network   -e KAFKA_BROKERCONNECT=kafka-server:9092  -e SERVER_SERVLET_CONTEXTPATH="/"  obsidiandynamics/kafdrop:latest
    ```

3. **Apache Airflow:** Envoiremntinizde kurulu olan Airflow'u başlatmak için aşağıdaki komutları kullanabilirsiniz
   ```bash
    airflow db reset
    airflow db init
    export AIRFLOW_HOME=/dosyanıznız/pathi
   airflow standalone
    ```

5. **Veritabanı:** Kendi tercihinize göre bir veritabanı oluşturun ve bağlantı yapılandırmalarını ayarlayın.
   ```bash
    docker run --name my_postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
    ```

## Kullanım

1. Airflow arayüzünden DAG'ı çalıştırın. Bu DAG, Kafka'dan verileri çeker ve veritabanına yazar.
2. Dizinde yer alan log kayıtlarını inceleyebilirsiniz.

