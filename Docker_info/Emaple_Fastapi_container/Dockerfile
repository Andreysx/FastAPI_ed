# pull the official base image
FROM python:3.12.0-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /usr/src/app

# copy requirements.txt file to work directory
COPY requirements.txt .

# update pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project to work directory
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]