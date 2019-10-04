FROM ubuntu:18.04
LABEL mantainer "softway4IoT"

RUN apt update && apt upgrade

RUN apt install net-tools

RUN apt -y install wget

RUN wget https://github.com/etcd-io/etcd/releases/download/v3.3.13/etcd-v3.3.13-linux-amd64.tar.gz

RUN tar xvf etcd-v3.3.13-linux-amd64.tar.gz
RUN cd etcd-v3.3.13-linux-amd64 && mv etcd etcdctl /usr/local/bin

ADD make_it_running.py /home

CMD ["etcd"]

