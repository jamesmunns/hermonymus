from debian:jessie

# Yeah, python3 is really picky about UTF-8. This seems to make it happy.
RUN apt-get update -qq && \
    apt-get install -y locales -qq && \
    locale-gen en_US.UTF-8 en_us && \
    dpkg-reconfigure locales && \
    dpkg-reconfigure locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8

ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get install -y python3 python3-pip cron git-core

RUN pip3 install flask flask_httpauth markdown slacker

ADD run.sh /run.sh

CMD ["/bin/bash", "/run.sh"]
