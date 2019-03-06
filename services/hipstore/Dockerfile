FROM ubuntu:18.04

EXPOSE 7878

RUN apt-get update
RUN apt-get -y install socat

WORKDIR /root/
COPY . .
RUN chmod +x /root/main
CMD ["socat", "-T", "4", "tcp-l:7878,reuseaddr,fork", "exec:/root/main"]
