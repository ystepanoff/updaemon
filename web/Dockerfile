FROM python:3.9
ARG CACHEBUST=1
COPY ./web /opt/web
COPY ./updaemon.conf /opt/updaemon.conf
WORKDIR /opt/web
RUN pip3 install --no-cache-dir -q -U virtualenv
ENV VIRTUALENV /opt/venv
RUN virtualenv -p python3 $VIRTUALENV
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -q -r /opt/web/requirements.txt
CMD . /opt/venv/bin/activate && flask run --host="0.0.0.0"
