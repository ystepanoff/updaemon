FROM debian:stable

RUN apt-get -qq -y update \
    && apt-get -qq -y install locales python3 python3-pip cron \
    && apt-get -qq -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && localedef -i en_GB -c -f UTF-8 -A /usr/share/locale/locale.alias en_GB.UTF-8

COPY . /opt/updaemon
WORKDIR /opt/updaemon

RUN pip3 install --no-cache-dir -q -U virtualenv
ENV VIRTUALENV /opt/venv
RUN virtualenv -p python3 $VIRTUALENV

COPY requirements.txt /tmp/
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -q -r /tmp/requirements.txt

ADD crontab /etc/cron.d/updaemon
RUN chmod 0644 /etc/cron.d/updaemon

RUN touch /var/log/cron.log