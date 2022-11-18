# ReVanced Polling API

_We do a little polling ඞ_

![License: AGPLv3](https://img.shields.io/github/license/revanced/revanced-polling-api)
![GitHub last commit](https://img.shields.io/github/last-commit/revanced/revanced-polling-api)
![GitHub Workflow Status](https://github.com/revanced/revanced-polling-api/actions/workflows/dev.yml/badge.svg)

This is a simple API that returns the latest ReVanced releases, patches and contributors.

## Usage

The API is available at [https://poll.revanced.app//](https://poll.revanced.app/).

You can deploy your own instance by cloning this repository, editing the `docker-compose.yml` file to include your GitHub token and running `docker-compose up` or `docker-compose up --build` if you want to build the image locally instead of pulling from GHCR. Optionally you can run the application without Docker by running `poetry install` and `poetry run ./run.sh`. In this case, you'll also need a redis server and setup the following environment variables on your system.

| Variable               | Description                                      |
| ---------------------- | ------------------------------------------------ |
| `REDIS_URL`            | The hostname/IP of your redis server.            |
| `REDIS_PORT`           | The port of your redis server.                   |
| `HYPERCORN_HOST`       | The hostname/IP of the API.                      |
| `HYPERCORN_PORT`       | The port of the API.                             |
| `SENTRY_DSN`           | The DSN of your Sentry instance.                 |
| `CLIENT_ID`            | The ID to be used by your auth client.           |
| `CLIENT_SECRET`        | The secret to be used by your auth client.       |
| `SECRET_KEY`           | The key used to encrypt your PASETO tokens.      |


Please note that there are no default values for any of these variables.

If you don't have a Sentry instance, we recommend using [GlitchTip](https://glitchtip.com/).

### API Endpoints

* [logos](https://poll.revanced.app/logos) - Returns all the logos submited to evaluation
* [ballot](https://poll.revanced.app/ballot) - Casts a ballot on the logo polling

## Authentication

The API uses [PASETO](https://paseto.io/) tokens for authorization. To authenticate, you need to send a POST request to `/auth` with the following JSON body:

```json
{
  "id": "your_client_id",
  "secret": "your_client_secret",
  "discord_id_hash": "your_discord_id_hash"
}
```

The API will answer with a PASETO token that you can use to authorize your requests. You can use the token in the `Authorization` header of your requests, like this:

```
Authorization: Bearer <token>
```

That token will be valid for 5 minutes. After that, you'll need to generate a new one.

## Contributing

If you want to contribute to this project, feel free to open a pull request or an issue. We don't do much here, so it's pretty easy to contribute.

## License

This project is licensed under the AGPLv3 License - see the [LICENSE](LICENSE) file for details.
