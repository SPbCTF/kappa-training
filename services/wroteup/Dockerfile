FROM golang:latest

ENV GOPATH /go
ENV CGO_ENABLED 1
EXPOSE 50000

WORKDIR $GOPATH/src/github.com/kappactf/spbctf-20190303/services/wroteup/
RUN go get github.com/mattn/go-sqlite3
COPY . .

ENTRYPOINT ["go", "run", "main.go"]
