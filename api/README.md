# Brain Project API

This directory contains the FastAPI-based REST API for the Brain Project, providing a web interface to interact with the CognitiveCrew system.

## Setup

1. Install the API dependencies:
```bash
pip install -r api_requirements.txt
```

2. Run the API server:
```bash
python api/main.py
```

The server will start on http://localhost:8000 by default.

## API Endpoints

### POST /api/process
Process input through the CognitiveCrew system.

**Request Body:**
```json
{
    "input": "Your input text here",
    "domain": "optional domain specification"
}
```

**Response:**
```json
{
    "status": "success",
    "result": {
        // Processing results here
    }
}
```

### GET /api/health
Check the API server health.

**Response:**
```json
{
    "status": "healthy"
}
```

## Web Interface

The API serves a web interface from the `/web` directory. Access it by opening http://localhost:8000 in your browser.

## Development

- The server runs in development mode with auto-reload enabled
- CORS is configured to allow all origins (modify for production)
- Static files are served from the `web` directory

## Environment Variables

- `PORT`: Server port (default: 8000)
- `OPENAI_API_KEY`: Your OpenAI API key (required for CognitiveCrew)

## Production Deployment

For production deployment:

1. Set appropriate CORS origins
2. Disable auto-reload
3. Configure proper security measures
4. Use a production-grade ASGI server