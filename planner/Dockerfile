FROM ubuntu:20.04

WORKDIR /planner
COPY . /planner

RUN apt-get -y update
RUN apt-get -y install git curl

RUN mkdir deps && cd deps \
 &&  curl https://download.java.net/openjdk/jdk12/ri/openjdk-12+32_linux-x64_bin.tar.gz --output java.tar.gz \
 && tar xvf java.tar.gz \
 && rm -f ./java.tar.gz
ENV JAVA_HOME="/planner/deps/jdk-12"
ENV PATH="/planner/deps/jdk-12/bin:${PATH}"

RUN cd deps && git clone https://github.com/uwe-koeckemann/AIDDL.git \
 && cd AIDDL \
 && git checkout develop

RUN cd deps/AIDDL/core/java/ && ./gradlew publishToMavenLocal \
 && cd   ../../util/java/ && ./gradlew publishToMavenLocal \
 && cd    ../../common/java/ && ./gradlew publishToMavenLocal


RUN ./gradlew build

ENV AIDDL_PATH="/planner/AIDDL/core/aiddl:/planner/AIDDL/common/aiddl"

EXPOSE 8061

CMD [ "./gradlew", "run" ]
