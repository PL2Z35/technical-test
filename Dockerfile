FROM python:3.11-slim

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# docker run -p 8000:8000 --env-file ./app/.env cristian9923/chainstore:latest   
# docker build -t cristian9923/chainstore:latest .    