FROM python:3.12.4
LABEL authors="maskira"

COPY . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python -m flask run --host=0.0.0.0 --port=5000