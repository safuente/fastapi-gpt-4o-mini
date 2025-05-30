# GPT-4o-mini Model API

A RESTful API built with FastAPI to interface with the GPT-4o-mini language model. It offers features such as text summarization, sentiment analysis, translation, and text completion. This project is designed for modularity, security, and scalability.

---

## Requirements

To run the application, ensure the following tools are installed:

* Docker
* Docker Compose

You may use:

* Docker Desktop (Windows/macOS)
* Rancher Desktop
* Podman (with Docker compatibility enabled)

---

## Getting Started

### Environment Configuration

Create a `.env` file at the project root with the following structure:

```env
FAKE_USERNAME=test_user
FAKE_PASSWORD=1234
JWT_SECRET=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

These settings are loaded via `pydantic-settings` in `config.py`.

### Default User Credentials

A default user was configured for testing purpose

* **Username**: `test_user`
* **Password**: `1234`

You can change these in the `.env` file.

A token must be obtained through the `/auth/login` endpoint and added to the Swagger docs using the **Authorize** button.

---

## API Usage

Once up, access to api documentation here:

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

---

## Makefile Commands

| Command      | Description                                |
| ------------ | ------------------------------------------ |
| `make up`    | Start the development environment          |
| `make upd`   | Start in detached mode                     |
| `make down`  | Stop and remove containers                 |
| `make stop`  | Stop containers                            |
| `make build` | Force Docker image build                   |
| `make rm`    | Remove stopped containers                  |
| `make pull`  | Pull latest images                         |
| `make test`  | Run all unit tests                         |
| `make lint`  | Run linter (Black)                         |
| `make bash`  | Open an interactive shell in the container |

---

## Architecture Overview

### Modular Routers

Each functionality (summarize, translate, complete, analyze, auth) is isolated in its own router for clean separation of concerns and scalability.

### Exception Handling

Custom exception handling ensures consistent error responses and better debugging.

### JWT Authentication

JWT-based authentication is enforced, with a default user and secret configurable via `.env`. The Swagger UI is integrated with Bearer Auth.

### Rate Limiting

Rate limiting is enabled using `slowapi` to protect the service from abuse.

### Logging

Structured logging class is used in the app.

### Documentation

Auto-generated API documentation via FastAPI:

* Swagger: interactive testing
* ReDoc: detailed schema and descriptions

---

## Scalability and Best Practices

This project is structured for scalability and ensuring best practices:

* **Separation of routers** by functionalities
* **Separation of services** by functionalities using a base service
* **Use of schemas** for input/output data validations
* **Centralized config** using `pydantic`
* **Dependency injection** for auth
* **Unit testing** for routers and services
* **Black** for PEP8 format
* **Environment-driven** settings via `.env`
* **Dockerized** for easy deployment across environments

---

## Why GPT-4o-mini?
The GPT-4o-mini model was chosen due to its excellent balance between 
performance and cost-effectiveness. With a significantly lower cost per 
token compared to larger models, it is ideal for real-time, scalable APIs 
that serve summarization, translation, and analysis tasks. 
Its compact size ensures faster response times while still offering strong 
capabilities in natural language understanding and generation.

| Token Type | Price per 1 Million Tokens |
|------------|---------------------------|
| Input      | $0.15                     |
| Output     | $0.60                     |

Example Cost
If you send 1,000 input tokens and receive 500 output tokens:

Input: (1,000 / 1,000,000) × $0.15 = $0.00015

Output: (500 / 1,000,000) × $0.60 = $0.0003

Total: $0.00045

GPT-4o consistently outperforms GPT-4o mini across benchmarks, 
achieving around 88.7% on MMLU compared to GPT-4o mini's 82.0%, 
representing only a 6-8% performance advantage. 
However, GPT-4o mini provides faster response times 
and is significantly more cost-effective, making it ideal 
for simpler tasks while the full model excels at complex reasoning 
and advanced programming. Because of that I think is a correct decision 
for this project.

## Potential Improvements

* Add **load testing** for the API with Locust. Here there is an example from my Medium´s profile:
[Go to the article
](https://medium.com/@santiagoalvarez87/building-a-real-time-traffic-api-with-fastapi-redis-pub-sub-and-load-testing-using-locust-3e42c6404ed5)
* Implement **Redis cache** for repeated queries to save costs
* Integrate **PostgreSQL** or another database for user/session persistence
* Use **Kubernetes** for advanced deployments
* Add **OpenTelemetry** or **Prometheus** for observability

---

## License

This project is open-source and available under the MIT License.
