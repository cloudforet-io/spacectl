FROM python:3.8

ENV SRC_DIR /tmp/src
RUN pip3 install --upgrade pip && \
    pip3 install --upgrade spaceone-core spaceone-api --pre

COPY src ${SRC_DIR}

WORKDIR ${SRC_DIR}
RUN python3 setup.py install && rm -rf /tmp/*
WORKDIR /root
# you can mount spacectl configurations on /root/.spaceone/
ENTRYPOINT ["spacectl"]
