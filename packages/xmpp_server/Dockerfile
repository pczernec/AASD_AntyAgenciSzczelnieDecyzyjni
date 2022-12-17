FROM ubuntu:22.10

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
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

COPY prosody_modules /usr/lib/prosody/modules


# https://github.com/docker-library/redis/blob/master/Dockerfile.template

RUN mkdir /data && chown prosody:prosody /data
VOLUME /data

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]
