# Vision Web Worker

* [Flask](https://flask.palletsprojects.com/en/2.1.x/), to manage the network connection
* [gunicorn](https://gunicorn.org/), for production deployment
* [requests](https://docs.python-requests.org/en/latest/), to handle contacting the ashirt instance
* [structlog](https://www.structlog.org/en/stable/), for structured logging
* [python-dotenv](https://pypi.org/project/python-dotenv/), for environment loading (this is primarily aimed at development)

In addition, this service tries to be as type-safe as possible, so extra effort has been provided to ensure that the typing is specified as much as possible.

To get up and running, open the project root in a terminal, install pipenv, and run `pipenv shell`, then `pipenv install`

## Deploying to AShirt

The typical configuration for deploying this worker archetype is going to look roughly like this:

```json
{
    "type": "web", 
    "version": 1,
    "url": "http://vision-web/process"
}
```

Note the url: this is likely what will change for your version.

## Adding custom logic

Most programs should be able to largely ignore most of the code, and instead focus on `actions` directory, and specifically the events you want to target.

## Integrating into AShirt testing environment

Notably, the dev port exposed is port 8080, so all port mapping has to be done with that in mind. When running locally (not via docker), the exposed port is configurable.

This configuration should work for your scenario, though the volumes mapped might need to be different.

```yaml
  vision-web:
    build:
      context: ashirt-workers/workers/vision-web
      dockerfile: Dockerfile.dev
    ports:
      - 3004:8080
    restart: on-failure
    volumes:
      - ./ashirt-workers/workers/vision-web/:/app/
    environment:
      ENABLE_DEV: true
      ASHIRT_BACKEND_URL: http://backend:3000
      ASHIRT_ACCESS_KEY: gR6nVtaQmp2SvzIqLUWdedDk
      ASHIRT_SECRET_KEY: WvtvxFaJS0mPs82nCzqamI+bOGXpq7EIQhg4UD8nxS5448XG9N0gNAceJGBLPdCA3kAzC4MdUSHnKCJ/lZD++A==
```


Note that the mapped volume overwrites the source files placed in the image. This allows for hot-reloading of the worker when deployed to docker-compose. If you don't want or need hot reloading, then you can simply omit this declaration.
