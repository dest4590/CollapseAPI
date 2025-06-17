# CollapseAPI

A Django REST API platform for managing and distributing secure Minecraft clients.

## Overview

CollapseAPI provides service for Minecraft clients, tracking downloads, launches, and client metadata.
This API is designed to support the CollapseLoader ecosystem, providing a secure platform for distributing Minecraft clients.

## Features

-   **Client Management**: Store and manage Minecraft client information
-   **Download Tracking**: Track client download statistics
-   **Launch Tracking**: Monitor client usage statistics
-   **REST API**: Full-featured API for integrating with other services
-   **API Documentation**: Built-in Swagger documentation

## Tech Stack

-   Python 3.12
-   Django
-   Django REST Framework
-   Docker support

## Installation

### Prerequisites

-   Python 3.12 or higher
-   pip (Python package manager)

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/dest4590/CollapseAPI.git
    cd CollapseAPI
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:

    ```bash
    python manage.py migrate
    ```

4. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Client Management

-   `GET /clients/` - List all clients
-   `POST /clients/` - Create a new client
-   `GET /clients/{id}/` - Get client details
-   `PUT /clients/{id}/` - Update client details
-   `DELETE /clients/{id}/` - Delete client

### Usage Tracking

-   `POST /api/client/{id}/launch/` - Record a client launch
-   `POST /api/client/{id}/download/` - Record a client download

## API Documentation

API documentation is available at `/swagger/`

## Contributing

Contributions are welcome. Please feel free to submit a Pull Request.
