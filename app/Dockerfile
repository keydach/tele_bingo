FROM python:3.10-slim-buster

RUN echo 'deb http://mirror.yandex.ru/debian buster main contrib non-free' > /etc/apt/sources.list && \
    echo 'deb http://mirror.yandex.ru/debian buster-updates main contrib non-free' >> /etc/apt/sources.list && \
    echo 'deb http://security.debian.org buster/updates main contrib non-free' >> /etc/apt/sources.list && \
    echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen && \
    echo 'ru_RU.UTF-8 UTF-8' >> /etc/locale.gen && \
    echo 'LANG=en_US.UTF-8' > /etc/default/locale && \
    echo 'Asia/Yekaterinburg' > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Asia/Yekaterinburg /etc/localtime && \
    apt-get update && \
    apt-get install -y wkhtmltopdf

WORKDIR app
ENV PYTHONPATH "/"

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . app
CMD ["python3", "main.py"]
