FROM python:3

COPY /worker /app/worker

WORKDIR /app
RUN pip install -r worker/requirements.txt

CMD ["/usr/local/bin/python", "worker/worker.py"]
