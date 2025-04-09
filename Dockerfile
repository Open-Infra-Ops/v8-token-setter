FROM openeuler/openeuler:24.03-lts

RUN yum install -y vim wget git xz tar make automake autoconf libtool gcc gcc-c++ kernel-devel libmaxminddb-devel pcre-devel openssl openssl-devel tzdata \
    readline-devel libffi-devel python3-devel mariadb-devel python3-pip net-tools.x86_64 iputils && \
    groupadd -g 1000 robot && \
    useradd -u 1000 -g robot -s /bin/bash -m robot && \
    mkdir -p /work/v8-token-setter && chown -R 1000:1000 /work/v8-token-setter && \
    mkdir -p /vault/secrets && chown -R 1000:1000 /vault/secrets

WORKDIR /work/v8-token-setter

COPY --chown=robot . /work/v8-token-setter

USER robot

RUN cd /work/v8-token-setter && \
    python3 -m venv venv && ./venv/bin/pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV LANG=en_US.UTTF-8 \
    PYTHONPATH=/work/v8-token-setter \
    PATH=/work/v8-token-setter/venv/bin:$PATH

ENTRYPOINT ["/work/v8-token-setter/venv/bin/uwsgi", "--ini", "/work/v8-token-setter/deploy/production/uwsgi.ini"]