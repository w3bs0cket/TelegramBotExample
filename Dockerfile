FROM python:3.12-slim

WORKDIR /app

COPY bot.py /app/

COPY requirements.txt /app/

COPY src /app/src/

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]