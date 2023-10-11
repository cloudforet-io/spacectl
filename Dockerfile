FROM cloudforet/python-core:1.12

ENV SRC_DIR /tmp/src
ENV SPACECTL_DEFAULT_ENVIRONMENT default

COPY pkg/pip_requirements.txt pip_requirements.txt

RUN apt-get update && apt-get install vim -y  \
    && pip install --upgrade -r pip_requirements.txt

COPY src ${SRC_DIR}
WORKDIR ${SRC_DIR}

RUN python3 setup.py install && rm -rf /tmp/*

RUN pip install --upgrade spaceone-api

WORKDIR /root

CMD ["tail", "-f", "/dev/null"]
