FROM openeuler/openeuler:22.03-lts

MAINTAINER liuqi<469227928@qq.com>

RUN yum install -y vim wget git xz tar make automake autoconf libtool gcc gcc-c++ kernel-devel libmaxminddb-devel pcre-devel openssl openssl-devel tzdata \
readline-devel libffi-devel python3-devel mariadb-devel python3-pip net-tools.x86_64 iputils

WORKDIR /work/v8-token-setter

COPY . /work/v8-token-setter

RUN cd /work/v8-token-setter && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV LANG=en_US.UTTF-8

ENTRYPOINT ["uwsgi", "--ini", "/work/v8-token-setter/deploy/production/uwsgi.ini"]
