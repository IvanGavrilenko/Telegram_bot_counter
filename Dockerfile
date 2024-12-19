FROM ultralytics/ultralytics:latest-python

ENV TELEGRAM_TOKEN="1234:ABCDEFG"

RUN pip install pytelegrambotapi pillow

WORKDIR /code  

COPY . /code  

CMD [ "python", "./docker_telegram_bot.py" ]