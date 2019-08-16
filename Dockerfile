FROM python:3

ENV HOME=/code
RUN mkdir -p ${HOME} && \
    useradd -u 1001 -r -g 0 -d ${HOME} -s /sbin/nologin \
            -c "David Lightman" default
WORKDIR ${HOME}

ADD wopr ${HOME}/wopr
ADD requirements.txt setup.py ${HOME}/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

RUN chown -R 1001:0 ${HOME} && \
    find ${HOME} -type d -exec chmod g+ws {} \;

USER 1001

CMD [ "python", "./wopr/dialer.py" ]
