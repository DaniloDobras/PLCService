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
git clone https://github.com/your-org/PLCService.git
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
alembic upgrade head
```

Generate new revision:

```bash
alembic revision --autogenerate -m "added new table"
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

## 📢 Kafka Topics

* **Consumed**: `orders`
* **Produced**: `plc-status`

Example consumed message:

```json
{
  "bucketId": "B123",
  "materialId": "M456",
  "qty": 10
}
```

Example produced message:

```json
{
  "status": "processed",
  "bucketId": "B123",
  "timestamp": "2025-07-21T10:45:00Z"
}
```

---

## Tech Stack

* FastAPI
* SQLAlchemy
* Kafka (via `kafka-python`)
* OPC UA (`asyncua` assumed)
* PostgreSQL
* Docker

---
