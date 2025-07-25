# PLCService - PLC Integration Microservice

A FastAPI-based microservice that listens to Kafka messages from the `orders` topic, stores them in a database, and publishes processed results to the `plc-status` topic. It also communicates with an OPC UA server.

---

## 📁 Project Structure

```
PLCService/
├── alembic/               # Alembic for database migrations
│   └── versions/          # Versioned migration scripts
├── app/                   # Application logic
│   ├── api/               # API module (FastAPI setup)
│   │   └── __init__.py
│   ├── core/              # Core services
│   │   ├── config.py      # Environment config
│   │   └── kafka_worker.py # Kafka consumer/producer logic
│   ├── db/                # DB layer
│   │   ├── database.py    # SQLAlchemy session
│   │   └── models.py      # DB models
│   └── main.py            # Application entrypoint
├── .env.template          # Environment variable template
├── docker-compose.yml     # Docker multi-service config
├── Dockerfile             # Container build config
├── requirements.txt       # Python dependencies
├── alembic.ini            # Alembic config
└── test_main.http          # HTTP test script
```

---

## Features

* ✅ Kafka Consumer (orders topic)
* ✅ Kafka Producer (plc-status topic)
* ✅ OPC UA integration
* ✅ PostgreSQL database
* ✅ Dockerized deployment
* ✅ Alembic migrations

---

##  Setup

### 1. Clone the repository

```bash
git clone https://github.com/DaniloDobras/PLCService.git
cd PLCService
```

### 2. Environment Variables

Create a `.env` file:

```bash
cp .env.template .env
```

### .env content:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=plc
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@plc-db:5432/${POSTGRES_DB}

KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_CONSUME_TOPIC=orders
KAFKA_PRODUCE_TOPIC=plc-status

OPCUA_ENDPOINT=opc.tcp://host.docker.internal:62640/IntegrationObjects/ServerSimulator
```

---

##  Run with Docker

```bash
docker-compose up --build
```

> Ensure Kafka, PostgreSQL, and the OPC UA Server are accessible in your Docker network.

---

## Alembic Migrations

Run database migration:

```bash
docker exec -it plc-service alembic upgrade head
```

Generate new revision:

```bash
docker exec -it plc-service alembic revision --autogenerate -m "table added"
```

---

## OPC UA Server Integration

### Required:

* [Integration Objects OPC UA Simulator](https://integrationobjects.com/sioth-opc/sioth-opcunified-architecture/opc-ua-server-simulator/)
* Properly exposed OPC UA endpoint (locally and/or via Docker)
* Example endpoint: `opc.tcp://host.docker.internal:62640/IntegrationObjects/ServerSimulator`

### For Monitoring:

* Use [Unified Automation UA Expert](https://www.unified-automation.com/products/development-tools/uaexpert.html) to monitor and inspect the OPC UA Server.

---

## Kafka Topics

* **Consumed**: `orders`
* **Produced**: `plc-status`

Example consumed message:

```json
{
  "order_id": 42,
  "priority": 1,
  "buckets": [
    {
      "bucket_id": 1001,
      "material_type": "Steel",
      "material_qty": 2,
      "position": {
        "position_x": 10,
        "position_y": 5,
        "position_z": 0
      }
    },
    {
      "bucket_id": 1002,
      "material_type": "Aluminum",
      "material_qty": 3,
      "position": {
        "position_x": 12,
        "position_y": 7,
        "position_z": 0
      }
    }
  ]
}

```

Example produced message:

```json
{
  "orderId": 1,
  "bucketId": 1,
  "materialId": "Steel",
  "qty": 5,
  "position": {
        "position_x": 12,
        "position_y": 7,
        "position_z": 0
      },
  "status": "accepted",
  "source": "PLCService"
}
```

---

## Tech Stack

* FastAPI
* SQLAlchemy
* Kafka (via `kafka-python`)
* OPC UA (`opcua`)
* PostgreSQL
* Docker

---
