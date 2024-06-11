FROM python:3.12.4
LABEL authors="maskira"

COPY . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python app.py