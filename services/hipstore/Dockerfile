FROM ubuntu:18.04

EXPOSE 7878

RUN apt-get update
RUN apt-get -y install socat

WORKDIR /root/
COPY . .
RUN mkdir /root/users
RUN chmod +x /root/main
CMD ["socat", "-T", "10", "-d", "-d", "tcp-l:7878,reuseaddr,fork", "exec:/root/main"]
