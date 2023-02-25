FROM python:3-slim

WORKDIR /app
ADD . .
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python3", "run.py"]
