from kafka import KafkaConsumer, KafkaProducer
import json
from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models import PLCCommand

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def handle_kafka_messages():
    print("Starting Kafka consumer...")

    consumer = KafkaConsumer(
        settings.KAFKA_CONSUME_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id="plc-consumer",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    print(f"Connected to topic: {settings.KAFKA_CONSUME_TOPIC}")
    db = SessionLocal()
    for message in consumer:
        print(f"Consumed message: {message}")
        data = message.value

        plc_command = PLCCommand(
            bucket_id=data["bucketId"],
            material_id=data["materialId"],
            qty=data["qty"]
        )
        db.add(plc_command)
        db.commit()

        new_message = {
            "bucketId": data["bucketId"],
            "status": "accepted",
            "source": "PLCService"
        }
        producer.send(settings.KAFKA_PRODUCE_TOPIC, new_message)
        producer.flush()
