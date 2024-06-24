# Vision Lambda Python

This is a worker for using phi-3-vision with image evidence. While this might be useful for your purposes, you will likely want to spend time tuning your worker to answer specific questions of evidence. Use the `VISION_QUESTIONS` environment variable to define what you what to ask.

## Typical Configuration

```ts
{
    "type": "aws", 
    "version": 1,
    "lambdaName": "vision",
    "asyncFunction": true
}
```

## Testing with Docker Compose / Standard development environment

The following docker-compose configuration section should work:

```yml
  vision:
    build:
      context: ashirt-workers/vision-lambda-python
      dockerfile: Dockerfile
    ports:
      - 3003:8080
    restart: on-failure
    environment:
      ASHIRT_BACKEND_URL: http://backend:3000
      # Note that these below values are pre-set in the standard database seed
      ASHIRT_ACCESS_KEY: gR6nVtaQmp2SvzIqLUWdedDk
      ASHIRT_SECRET_KEY: WvtvxFaJS0mPs82nCzqamI+bOGXpq7EIQhg4UD8nxS5448XG9N0gNAceJGBLPdCA3kAzC4MdUSHnKCJ/lZD++A==
      VISION_QUESTIONS: ""What does the image say?,Which times are shown in the image?, Which applications are open in the image?, Which operating system is being used in the image?"
```
