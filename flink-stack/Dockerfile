FROM alpine:latest
RUN apk add --no-cache curl inotify-tools
COPY hot-reload.sh /hot-reload.sh
RUN chmod +x /hot-reload.sh
WORKDIR /opt/src
ENTRYPOINT ["/hot-reload.sh"]