# Google Vision OCR Worker

A microservice worker built on Python/Flask that uses Google Cloud Vision API to perform OCR on image evidence.

## How it works

When new image evidence is added to AShirt, this worker:
1. Retrieves the image data from the AShirt backend
2. Sends it to the [Google Cloud Vision API](https://cloud.google.com/vision/docs) for text detection
3. Returns the extracted OCR text to AShirt as evidence metadata

## Prerequisites

- Docker and Docker Compose
- Google Cloud project with Vision API enabled
- Google Cloud service account credentials JSON file
- AShirt backend running

## Setup

### 1. Configure environment variables

Copy `.env.example` to `.env` and fill in the required values:

```bash
cp .env.example .env
```

Required variables:
- `ASHIRT_BACKEND_URL` - URL of the AShirt backend (e.g., `http://backend:3000` when using Docker networking)
- `ASHIRT_ACCESS_KEY` - Access key from an AShirt headless user account
- `ASHIRT_SECRET_KEY` - Secret key (base64 format) from an AShirt headless user account
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Google Cloud credentials JSON file inside the container (e.g., `/credentials.json`)
- `ENABLE_DEV` - Set to `true` for development mode with extra logging

### 2. Google Cloud credentials

1. Create a service account in Google Cloud Console with Vision API access
2. Download the JSON credentials file
3. Mount it into the container (see docker-compose.yml) at the path specified in `GOOGLE_APPLICATION_CREDENTIALS`

### 3. Run the worker

```bash
make run_dev
```

Or manually:

```bash
docker compose up --build
```

The worker will be available on port 9000 (configurable in docker-compose.yml).

## Deploying to AShirt

Register the worker in AShirt with this configuration:

```json
{
  "url": "http://gcp-vision:9000/ashirt/process",
  "type": "web",
  "version": 1
}
```

**Note:** The URL depends on your deployment:
- If running with Docker Compose on the same network: `http://gcp-vision:9000/ashirt/process`
- If running separately: Use the appropriate host and port

## Docker Networking

This worker must be on the same Docker network as the AShirt backend. See `docker-compose.yml` for network configuration.
