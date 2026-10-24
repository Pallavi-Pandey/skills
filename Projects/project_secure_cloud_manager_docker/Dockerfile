FROM python:3.12-slim

WORKDIR /app

# The build context is the Projects directory. Reuse the same application code
# as the local beginner project instead of maintaining a second copy.
COPY project_secure_cloud_manager/ /app/

ENV PYTHONUNBUFFERED=1

EXPOSE 5050

CMD ["python3", "cloud_server.py"]
