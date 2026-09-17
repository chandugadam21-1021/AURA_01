from pathlib import Path


class MessagingDetectionModule:

    MESSAGING_DEPENDENCIES = {

        # RabbitMQ
        "pika": "RabbitMQ",
        "aio-pika": "RabbitMQ",
        "amqp": "RabbitMQ",

        # Apache Kafka
        "kafka-python": "Apache Kafka",
        "confluent-kafka": "Apache Kafka",
        "kafkajs": "Apache Kafka",

        # Redis
        "redis": "Redis",
        "ioredis": "Redis",

        # Celery
        "celery": "Celery",

        # AWS SQS
        "boto3": "AWS SQS",

        # Google Cloud Pub/Sub
        "google-cloud-pubsub": "Google Cloud Pub/Sub",

        # Apache ActiveMQ
        "activemq": "ActiveMQ",

        # NATS
        "nats-py": "NATS",
        "nats": "NATS",

        # MQTT
        "paho-mqtt": "MQTT",
        "mqtt": "MQTT",

        # ZeroMQ
        "pyzmq": "ZeroMQ",
        "zeromq": "ZeroMQ",
    }

    MESSAGING_FILES = {
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "package.json",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "composer.json",
        "Gemfile",
        "go.mod",
        "Cargo.toml",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Messaging_Detector(self):

        detected_messaging_systems = []

        for file in self.files:

            if file.name not in self.MESSAGING_FILES:
                continue

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()

            except OSError:
                continue

            for dependency, messaging_system in (
                self.MESSAGING_DEPENDENCIES.items()
            ):

                if dependency.lower() in content:

                    if messaging_system not in detected_messaging_systems:
                        detected_messaging_systems.append(
                            messaging_system
                        )

        if not detected_messaging_systems:

            return {
                "primary_messaging": None,
                "messaging_systems": []
            }

        return {
            "primary_messaging": detected_messaging_systems[0],
            "messaging_systems": detected_messaging_systems
        }