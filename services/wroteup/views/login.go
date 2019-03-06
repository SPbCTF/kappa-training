package views

import (
	"crypto/sha512"
	"fmt"
	"github.com/kappactf/spbctf-20190303/services/wroteup/database"
	"github.com/kappactf/spbctf-20190303/services/wroteup/secrets"
	"html/template"
	"log"
	"net/http"
)

func Login(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("templates/login.html"))

	if r.Method == "GET" {
		log.Println(tmpl.Execute(w, nil))
	} else if r.Method == "POST" {
		if err := r.ParseForm(); err != nil {
			http.Error(w, "Can't parse form", http.StatusInternalServerError)
			return
		}

		login := r.Form.Get("login")
		password := r.Form.Get("password")

		db := database.Get()

		stmt, err := db.Prepare("select login, password from users where login = ? and password = ?")
		if err != nil {
			http.Error(w, "Can't prepare SQL", http.StatusInternalServerError)
			return
		}

		defer stmt.Close()

		var loginBuf, passwordBuf string

		err = stmt.QueryRow(login, password).Scan(&loginBuf, &passwordBuf)

		if err != nil {
			http.Error(w, "Invalid login/password", http.StatusForbidden)
			return
		}

		h := sha512.New384()
		h.Write([]byte(login + secrets.Salt))
		hash := fmt.Sprintf("%x", h.Sum(nil))

		cookie := &http.Cookie{Name: "KAPPA-AUTH", Value: login + "|" + hash, HttpOnly: true}
		http.SetCookie(w, cookie)

		http.Redirect(w, r, "/main", http.StatusMovedPermanently)

	} else {
		if _, err := fmt.Fprintln(w, "Unsupported method"); err != nil {
			http.Error(w, "Can't send response", http.StatusInternalServerError)
			return
		}
	}
}
