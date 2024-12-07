# Galaxy Quiz API

This repository contains the backend for the Galaxy Quiz web application. The application is built with Flask and uses MongoDB for data storage. The services are containerized using Docker to facilitate deployment and development.

## Features
- User authentication (Register, Login, Token Verification)
- JWT-based authentication with refresh tokens
- MongoDB as a data store for user information
- Docker-based setup for easy deployment and development

## Requirements
- Docker
- Docker Compose
- Python 3.9+

## Setup

### Clone the Repository
```bash 
git clone https://github.com/donttouchifworks/galaxy_quiz_backend.git
cd galaxy_quiz
```

## Configure environment for every service
### Auth service: 

example of configuration:

```bash
SECRET_KEY=your_secret_key_here
MONGO_URI=mongodb://mongo:27017
```
Mongo Database is configured in "docker-compose.yml",
if you want to use external MongoDB simply change mongodb://mongo:27017 to yours and 
delete next lines in "docker-compose.yml"
```bash
  mongo:
    image: mongo:latest
    container_name: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
```
and
```bash 
    depends_on:
      - mongo
```
in 
```bash 

  auth_service:
    image: auth_service_image
    env_file:
      - ./auth_service/.env
    build:
      context: ./auth_service
    ports:
      - "8001:8001"
    depends_on:
      - mongo
```
Otherwise, it will run a MongoDB inside container.




