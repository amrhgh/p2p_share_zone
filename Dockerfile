FROM python:3.8.3
COPY . /opt/pyTorrent
WORKDIR /opt/pyTorrent
RUN pip install -r requirements.txt