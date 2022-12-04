FROM ubuntu:22.10


RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        lsb-base \
        procps \
        adduser \
        lua-unbound \
        lua-bitop \
        lua-dbi-mysql \
        lua-dbi-postgresql \
        lua-dbi-sqlite3 \
        lua-event \
        lua-expat \
        lua-filesystem \
        lua-sec \
        lua-socket \
        lua-zlib \
        lua5.1 \
        lua5.2 \
        openssl \
        ca-certificates \
        ssl-cert \
        prosody \
        prosody-modules

EXPOSE 80 443 5222 5269 5347 5280 5281

RUN useradd -ms /bin/bash ubuntu
WORKDIR /home/ubuntu
COPY ./run.sh .

CMD ["./run.sh"]
