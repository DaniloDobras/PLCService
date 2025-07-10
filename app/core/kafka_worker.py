from kafka import KafkaConsumer, KafkaProducer
import threading, json, logging
from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models import PLCCommand

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def handle_kafka_messages():
    consumer = KafkaConsumer(
        settings.KAFKA_CONSUME_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id="plc-consumer",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    db = SessionLocal()
    for message in consumer:
        data = message.value
        logging.info(f"Consumed: {data}")

        # Store in DB
        plc_command = PLCCommand(
            bucket_id=data["bucketId"],
            material_id=data["materialId"],
            qty=data["qty"]
        )
        db.add(plc_command)
        db.commit()

        # Publish new status message
        new_message = {
            "bucketId": data["bucketId"],
            "status": "accepted",
            "source": "PLCService"
        }
        producer.send(settings.KAFKA_PRODUCE_TOPIC, new_message)
        producer.flush()
