FROM python:3.8-slim-buster

WORKDIR /gui

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /gui

RUN apt-get -y update
RUN apt-get -y install git libcairo2

RUN git clone https://github.com/uwe-koeckemann/AIDDL.git

ENV PYTHONPATH="/gui/AIDDL/core/python/src"
ENV AIDDL_PATH="/gui/AIDDL/core/aiddl:/gui/AIDDL/common/aiddl"

EXPOSE 8061

CMD [ "python3", "run.py" ]
