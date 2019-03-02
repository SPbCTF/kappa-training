package main

import (
	"github.com/kappactf/spbctf-20190303/services/wroteup/views"
	"log"
	"net/http"
)

func main() {

	http.HandleFunc("/login", views.Login)
	http.HandleFunc("/register", views.Register)

	http.HandleFunc("/post", views.PostWriteup)
	http.HandleFunc("/show", views.ShowWriteup)

	http.HandleFunc("/main", views.Main)

	log.Fatal(http.ListenAndServe(":50000", nil))
}
