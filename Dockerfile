FROM pytorrent_base:latest
COPY . /opt/pyTorrent
WORKDIR /opt/pyTorrent
RUN pip install -r requirements.txt
CMD python main.py