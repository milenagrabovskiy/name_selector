# slim version takes up less disk space
FROM python:3.12-slim

# creates working dir
WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

# This copies everything. Each command is a layer. requirements.txt will run first
COPY . .

# run the app!
CMD ["python", "main.py"]
