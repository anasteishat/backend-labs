# backend-labs

## api
healthcheck available at /health route

## launch instructions

### locally
- `python -m venv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`
- `flask run`

### docker
- `docker build -t app .`
- `docker run -p 5000:5000 app`

### docker compose
- `docker compose up --build`
