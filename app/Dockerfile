FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd --uid 10001 --system --no-create-home --shell /usr/sbin/nologin appuser
COPY --chown=10001:10001 . .

ENV APP_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000

USER 10001
CMD ["python", "main.py"]