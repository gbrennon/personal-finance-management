FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' --uid 1000 appuser

WORKDIR /app

RUN chown -R appuser:appuser /app

USER appuser

RUN python -m pip install --upgrade pip --user

COPY --chown=appuser:appuser requirements.txt .
RUN pip install --user -r requirements.txt

ENV PATH="/home/appuser/.local/bin:${PATH}"

COPY --chown=appuser:appuser . .

EXPOSE 8002

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
