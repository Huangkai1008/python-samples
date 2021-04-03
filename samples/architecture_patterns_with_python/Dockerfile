FROM python:3.9-slim-buster

WORKDIR app
COPY requirements.txt .

ENV FLASK_APP=flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
RUN pip install -i https://pypi.douban.com/simple -r requirements.txt
CMD flask run --host=0.0.0.0 --port=8000
