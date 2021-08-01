FROM python:3.6-slim

WORKDIR /app

VOLUME /outdir

COPY . .

#RUN apk update && apk upgrade && apk add ca-certificates && pip install -r requirements.txt
RUN apt update && apt upgrade -y && apt install -y ca-certificates wget && pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
