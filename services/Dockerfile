FROM python:3.8.3-slim
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install coverage

COPY app.py ./
COPY ./endpoints ./endpoints/
COPY ./resources ./resources/
COPY ./swagger ./swagger/
COPY ./utility ./utility/
COPY ./tests ./tests/
COPY ./logs ./logs/
COPY ./dataaccess ./dataaccess/
RUN chmod +x /app/app.py
RUN mkdir -p /var/log/jnjpythonservices/ \
	&& chmod -R +x /var/log/jnjpythonservices/
EXPOSE 9091
ENTRYPOINT [ "python3", "/app/app.py" ]
