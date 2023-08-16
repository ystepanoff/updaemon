FROM debian:buster

ARG CACHEBUST=1

RUN apt-get -qq -y update \
    && apt-get -qq -y install locales python3 python3-pip cron \
    && apt-get -qq -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && localedef -i en_GB -c -f UTF-8 -A /usr/share/locale/locale.alias en_GB.UTF-8

RUN pip3 install --no-cache-dir -q -U virtualenv
ENV VIRTUALENV /opt/venv
RUN virtualenv -p python3 $VIRTUALENV

COPY ./db /opt/db/
COPY ./updaemon.conf /opt/db/updaemon.conf
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -q -r /opt/db/requirements.txt
