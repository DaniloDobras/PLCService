from kafka import KafkaConsumer, KafkaProducer
import json
from app.core.config import settings
from opcua import Client, ua
from app.db.database import SessionLocal
from app.db.models import PLCCommand


producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def process_kafka():
    print("🚀 Starting Kafka consumer...")

    consumer = KafkaConsumer(
        settings.KAFKA_CONSUME_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id="plc-consumer",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    db = SessionLocal()
    opc_client = Client(settings.OPCUA_ENDPOINT)
    opc_client.connect()
    node_id = "ns=2;s=Tag7"
    node = opc_client.get_node(node_id)

    try:
        for message in consumer:
            data = message.value
            print(f"📥 Consumed message: {data}")

            order_id = data.get("order_id")
            buckets = data.get("buckets", [])

            for bucket in buckets:
                bucket_id = bucket["bucket_id"]
                material_id = bucket["material_type"]
                qty = bucket["material_qty"]
                position = bucket["position"]

                # Save to DB
                plc_command = PLCCommand(
                    message=str(data)
                )
                db.add(plc_command)

                # Prepare OPC UA message
                plc_result = {
                    "orderId": order_id,
                    "bucketId": bucket_id,
                    "materialType": material_id,
                    "qty": qty,
                    "position": position,
                    "status": "accepted",
                    "source": "PLCService"
                }

                # Write to OPC UA
                node.set_value(ua.Variant(json.dumps(plc_result), ua.VariantType.String))

                # Publish to Kafka
                producer.send(settings.KAFKA_PRODUCE_TOPIC, plc_result)

            db.commit()
            producer.flush()

    finally:
        opc_client.disconnect()
        db.close()


def start_kafka_consumer():
    """
    Starts Kafka consumer in a blocking loop (runs inside a background thread).
    """
    process_kafka()
