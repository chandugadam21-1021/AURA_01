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

    MESSAGING_DEPENDENCIES_LOWER = {
        dependency.lower(): messaging_system
        for dependency, messaging_system
        in MESSAGING_DEPENDENCIES.items()
    }

    MESSAGING_FILES_LOWER = {
        file.lower()
        for file in MESSAGING_FILES
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Messaging_Detector(self):

        detected_systems = set()

        for file in self.files:

            if file.name.lower() not in self.MESSAGING_FILES_LOWER:
                continue

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()
            except OSError:
                continue

            for dependency, messaging_system in (
                self.MESSAGING_DEPENDENCIES_LOWER.items()
            ):
                if dependency in content:
                    detected_systems.add(messaging_system)

        messaging_systems = sorted(detected_systems)

        return {
            "primary_messaging": (
                messaging_systems[0]
                if messaging_systems
                else None
            ),
            "messaging_systems": messaging_systems,
        }