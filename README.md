# FlaskAPP-python-container

A minimal Python Flask API packaged in a Docker container. This repository provides:
- app.py: simple in-memory REST API
- Dockerfile: builds a container running the app with Gunicorn
- requirements.txt: Python dependencies
- .dockerignore: files to ignore when building the image

## What it is
This is an example Flask service exposing a tiny REST API:
- GET / -> information about the service
- GET /ping -> health check (returns {"status":"ok"})
- GET /items -> list all items (in-memory)
- POST /items -> create an item with JSON body {"name": "..."}, returns 201 and created item
- GET /items/<id> -> get item by id
- PUT /items/<id> -> update an item's name with JSON body {"name": "..."}
- DELETE /items/<id> -> delete item

Note: storage is in-memory (a Python list). All data is lost when the process stops. Use a database for persistence.

## How it works
- The Flask app is defined in `app.py`. For local development you can run it directly with `python app.py`.
- For containerized production-like usage, the Dockerfile installs requirements and uses Gunicorn to serve the Flask application (`app:app`).

## Run locally (development)
1. Create & activate a virtual environment (optional but recommended)
   - python -m venv venv
   - source venv/bin/activate  (Linux/macOS) or venv\Scripts\activate (Windows)
2. Install dependencies
   - pip install -r requirements.txt
3. Run
   - python app.py
4. Open http://127.0.0.1:5000 or use curl:
   - curl http://127.0.0.1:5000/ping

## Build and run using Docker
1. Build the image:
   - docker build -t flaskapp-python-container:latest .
2. Run the container:
   - docker run -p 5000:5000 --rm --name flaskapp-example flaskapp-python-container:latest
3. Test endpoints:
   - curl http://localhost:5000/ping
   - curl http://localhost:5000/items
   - Create:
     curl -X POST -H "Content-Type: application/json" -d '{"name":"first"}' http://localhost:5000/items
   - Update:
     curl -X PUT -H "Content-Type: application/json" -d '{"name":"updated"}' http://localhost:5000/items/1
   - Delete:
     curl -X DELETE http://localhost:5000/items/1

## Notes and next steps
- Persistence: Replace the in-memory store with a database (SQLite, PostgreSQL, etc.) if you want data to survive restarts.
- Configuration: Add environment-based configuration and secrets management.
- Production: Consider adding logging, monitoring, and health checks suitable for orchestration (Kubernetes).
- Tests: Add unit and integration tests (pytest + requests).

If you want, I can:
- Add a database (SQLite or PostgreSQL) and update the Dockerfile/compose file.
- Add tests and a GitHub Actions workflow.
- Add example Kubernetes manifests.
Tell me which next step you prefer and I'll generate the files.
