FROM python:3.8-slim-buster

WORKDIR /gui

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /gui

RUN apt-get -y update
RUN apt-get -y install git

RUN git clone https://github.com/uwe-koeckemann/AIDDL.git \
 && cd AIDDL \                                            
 && git checkout develop

RUN git clone https://github.com/aiplan4eu/unified-planning.git

RUN cd /gui/AIDDL/core/python && pip install -e .
 
ENV AIDDL_PATH="/gui/AIDDL/core/aiddl:/gui/AIDDL/common/aiddl"

RUN jupyter trust ./unified-planning/notebooks/*.ipynb

EXPOSE 8061 8062

CMD [ "./start.sh" ]
