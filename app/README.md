# My FastAPI Application

This project is a FastAPI application that loads a machine learning model from a pickle file and exposes it through an API endpoint.

## Project Structure

```
app
├── app
│   ├── main.py              # Entry point of the FastAPI application
│   ├── api
│   │   └── endpoints.py     # API endpoints for the application
│   ├── models
│   │   └── model.pkl        # Serialized model in pickle format
│   └── tests
│       ├── __init__.py      # Marks the tests directory as a package
│       └── test_main.py     # Unit tests for the FastAPI application
├── Dockerfile                # Instructions to build a Docker image
├── requirements.txt          # Python dependencies for the project
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-fastapi-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

## Usage

Once the application is running, you can access the API at `http://127.0.0.1:8000`. The available endpoints can be explored using the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Running Tests

To run the tests, use the following command:
```
pytest app/tests
```

## Docker

To build and run the application using Docker, execute the following commands:

1. Build the Docker image:
   ```
   docker build -t app .
   ```

2. Run the Docker container:
   ```
   docker run -d -p 8000:8000 my-fastapi-app
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.