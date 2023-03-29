FROM python:alpine

ENV TZ "Asia/Yekaterinburg"

WORKDIR app
ENV PYTHONPATH "/"

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . app
CMD ["python3", "main.py"]
