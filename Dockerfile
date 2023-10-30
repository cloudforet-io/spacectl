FROM cloudforet/python-core:2.0

ENV SRC_DIR /tmp/src
ENV SPACECTL_DEFAULT_ENVIRONMENT default

COPY pkg/pip_requirements.txt pip_requirements.txt

RUN apt-get update && apt-get install vim -y  \
    && pip install --upgrade -r pip_requirements.txt

COPY src ${SRC_DIR}
WORKDIR ${SRC_DIR}

RUN python3 setup.py install && rm -rf /tmp/*

WORKDIR /root

CMD ["tail", "-f", "/dev/null"]
