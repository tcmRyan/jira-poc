FROM python:3

EXPOSE 5000

COPY /server /app/server
COPY config.py /app

WORKDIR /app
RUN pip install -r server/requirements.txt

CMD ["/usr/local/bin/gunicorn", "-b 0.0.0.0:5000", "server:app"]