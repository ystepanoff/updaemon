FROM python:3.9
COPY . /opt/web
WORKDIR /opt/web
RUN pip3 install --no-cache-dir -q -U virtualenv
ENV VIRTUALENV /opt/venv
RUN virtualenv -p python3 $VIRTUALENV
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -q -r /opt/web/requirements.txt
CMD . /opt/venv/bin/activate && python app.py
