FROM python:alpine3.19
RUN apk update && apk add --no-cache curl
WORKDIR /home/project/weather_app/
COPY . .
RUN pip install -r requirements.txt
