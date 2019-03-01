FROM ubuntu:18.04

EXPOSE 7878

RUN apt-get -y install socat

WORKDIR /root/
COPY . .
RUN mkdir /root/users
RUN chmod +x /root/main
CMD ["socat", "tcp-l:7878,fork,reuseaddr", "exec:/root/main"]
