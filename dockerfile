FROM python:3-slim

WORKDIR /programas/ingesta

# Instalar dependencias necesarias
RUN pip3 install boto3 mysql-connector-python pandas

COPY . .

CMD [ "python3", "./ingesta.py" ]
