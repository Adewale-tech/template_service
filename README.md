# Template Service

This service is part of the HNG Distributed Notification System and is responsible for managing email and push notification templates.

## Prerequisites

*   [Docker](https://www.docker.com/get-started)
*   [Git Bash](https://git-scm.com/downloads) (or any other terminal that can run curl)

## Configuration

The service has been configured to run with Docker Compose. The following files were created or modified:

*   `.env`: Contains the environment variables for the service, including database credentials and API keys.
*   `docker-compose.yml`: Defines the services, networks, and volumes for the application stack.
*   `app/core/config.py`: The application settings module has been updated to load the configuration from the `.env` file.

## Running the Service

1.  **Open Git Bash** in the project root directory (`c:\Users\ADEWALE\Template_workflow\template_service`).

2.  **Build and start the services** using Docker Compose:

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker image for the `template-service` and start all the services defined in `docker-compose.yml` (PostgreSQL, Redis, RabbitMQ, and the template service itself).

## Testing the Service

Once the services are running, you can test the `template-service` to ensure it's healthy and accessible.

### Using Git Bash

1.  **Open a new Git Bash terminal.**

2.  **Run the following curl command** to hit the health check endpoint:

    ```bash
           curl http://localhost:8082/health
    ```

3.  **You should see the following JSON response:**

    ```json
    {"success":true,"message":"Template Service is healthy and running.","data":null,"error":null}
    ```

### Using Your Browser

1.  **Open your web browser.**

2.  **Navigate to the following URL:**

    [http://localhost:8082/health](http://localhost:8082/health)

3.  You should see the same JSON response as above in your browser.

The full API documentation is available at [http://localhost:8082/docs](http://localhost:8082/docs) when the service is running.
curl http://localhost:8082/health
## Stopping the Service

To stop all the running services, press `Ctrl + C` in the terminal where `docker-compose up` is running, and then run:

```bash
docker-compose down
```

This will stop and remove the containers, networks, and volumes created by `docker-compose up`.
