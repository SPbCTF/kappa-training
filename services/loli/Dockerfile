FROM sollos/loli 

EXPOSE 4242

RUN apt-get -y install xinetd

WORKDIR /root/
COPY . . 
RUN mkdir /loli/users
RUN cp xinetd.conf /etc/xinetd.d/loli
RUN service xinetd restart

CMD script -c "xinetd -d"
