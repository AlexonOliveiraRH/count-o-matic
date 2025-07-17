# Deploying the Web Page Access Counter App with Podman

This guide will walk you through setting up and running the a simple and basic Flask Web Page Access Counter application using Podman. The intention is to have a lightweight and simplistic application that can be used to perform demonstrations involving the use of containers and pods in general, mainly with Podman.

## Prerequisites

- Podman installed on your system
- `podman-compose` installed (optional, but recommended)

## Project Structure

First, the project has the following directory and file structure:


```
count-o-matic/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── templates/
    └── index.html
```


## Step 1: Set Up the Project Files

1. Enter the directory for your project:

   ```
   $ cd count-o-matic
   ```


2. This is the list of the provided files with their correspondent artifacts:
   
   - `app.py` - The Flask application
   - `templates/index.html` - The HTML template with the stylish counter
   - `requirements.txt` - Python dependencies
   - `Dockerfile` - Container configuration
   - `docker-compose.yml` - Multi-container setup (optional)

## Step 2: Build the Container Image with Podman

### Option 1: Using Podman directly

1. Build the container image:

   ```
   $ podman build -t counter-app .
   ```

2. Create a pod for both containers:

   ```
   $ podman pod create --name counter-pod -p 8080:5000 -p 6379:6379
   ```


3. Run Redis in the pod:

   ```
   $ podman run -d --pod counter-pod --name redis \
     -v redis_data:/data:Z \
     docker.io/redis:alpine
   ```

4. Run your Flask application in the pod:

   ```
   $ podman run -d --pod counter-pod --name counter-app \
     -e REDIS_HOST=localhost \
     -e REDIS_PORT=6379 \
     localhost/counter-app
   ```

### Option 2: Using podman-compose (recommended)

If you have `podman-compose` installed (which provides Docker Compose-like functionality for Podman):

```
$ podman-compose up -d
```

This will build the image and start both containers as defined in the `docker-compose.yml` file.

## Step 3: Verify the Application

1. Check that your containers are running:

   ```
   $ podman pod ps
   $ podman ps
   ```

2. Test the health endpoint
   
   ```
   $ curl http://localhost:8080/health
   ```

3. Access the application in your web browser at:

   ```
   http://localhost:8080
   ```

You should see your stylish counter that increments each time you refresh the page.

## Step 4: Manage Your Application

- To stop the containers:

  ```
  $ podman-compose down  # if using podman-compose
  ```
  
  or

  ```
  $ podman pod stop counter-pod
  ```

- To start the containers again:

  ```
  $ podman-compose up -d  # if using podman-compose
  ```

  or

  ```
  $ podman pod start counter-pod
  ```
  

- To view logs:

  ```
  $ podman logs counter-app
  ```

## Persistent Storage

The Redis data is stored in a volume called `redis_data`, ensuring your counter values persist even if containers are restarted.

## Production Considerations

For a production environment:

1. Use a reverse proxy like Nginx or Traefik in front of your application
2. Set up proper TLS/SSL certificates
3. Consider using a more robust Redis setup with password protection
4. Implement health checks and automated restarts
5. Use container orchestration for larger deployments