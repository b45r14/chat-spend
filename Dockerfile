FROM python:3.11-slim-bookworm

RUN adduser --uid 1000 --disabled-password --gecos '' user

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/user/.local/bin:$PATH"

RUN pip install --user --no-cache-dir --upgrade pip

COPY . /app

WORKDIR /app

USER 1000

RUN pip install --user --no-cache-dir  --upgrade -r /app/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "/app/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]