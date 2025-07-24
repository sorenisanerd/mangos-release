FROM python:3 AS sumsbuilder

COPY requirements.txt main.py /build/

WORKDIR /build

RUN pip install -r requirements.txt
RUN --mount=type=secret,id=GITHUB_TOKEN,env=GITHUB_TOKEN python3 main.py

FROM caddy

ENV SITE_ADDRESS=http://127.0.0.1:8080

COPY --from=sumsbuilder /build/static/SHA256SUMS /usr/share/caddy/
COPY Caddyfile /etc/caddy/

