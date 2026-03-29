FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY adk_agent/ ./adk_agent/
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8000"]
