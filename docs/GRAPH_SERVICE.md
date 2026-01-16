# Neo4j Graph Service Setup

## Prerequisites

1. Neo4j database running (local or remote)
2. Python 3.13+
3. Environment variables configured

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Logfire Configuration (optional)
LOGFIRE_TOKEN=your_token
LOGFIRE_PROJECT_NAME=P_S_CQC_companion

# Application Configuration
ENV=development
DEBUG=true
```

You can also copy from `.env.example`:
```bash
cp .env.example .env
```

## Running the Application

1. Install dependencies:
```bash
uv sync
```

2. Start the application:
```bash
uvicorn src.app:app --reload
```

3. The API will be available at `http://localhost:8000`

## Available Endpoints

- **GET /health** - Health check endpoint that includes database status
- **Docs** - Interactive API documentation at `http://localhost:8000/docs`

## Observability

All database operations are automatically instrumented with Logfire. You can view:
- Request/response logging
- Database query execution times
- Error tracking and debugging information
- Custom span traces

Set `LOGFIRE_TOKEN` in `.env` to see logs in Logfire dashboard, or use local mode for development.
