FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY README.md README.md
COPY main.py main.py
COPY dashboard.py dashboard.py
COPY src src
COPY .python-version .python-version
COPY .streamlit .streamlit

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev
RUN pip install uv
RUN uv sync

EXPOSE 10000

CMD ["uv", "run", "main.py", "start-streamlit", "--port", "10000"]
