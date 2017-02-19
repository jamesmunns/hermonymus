from debian:jessie

RUN apt-get update

RUN apt-get install -y build-essential wget git-core zlib1g-dev ca-certificates openssl libssl-dev
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz && \
    tar xvf Python-3.6.0.tgz && \
    cd Python-3.6.0 && \
    ./configure && \
    make -j8 && \
    make install && \
    cd ../ && \
    rm Python-3.6.0.tgz && \
    rm -rf ./Python-3.6.0

RUN pip3 install flask flask_httpauth markdown slacker

RUN apt-get install -y cron

