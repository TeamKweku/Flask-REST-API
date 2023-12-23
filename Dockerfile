FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . .

# RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:5000 --access-logfile - "app:app"

