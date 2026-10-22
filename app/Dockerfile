FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime
LABEL org.opencontainers.image.source="https://github.com/DjZab/devops-portfolio"
WORKDIR /app
COPY --from=builder /install /usr/local
RUN useradd --uid 10001 --system --no-create-home --shell /usr/sbin/nologin appuser
COPY --chown=10001:10001 . .

ENV APP_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000

USER 10001

HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"]

CMD ["python", "main.py"]