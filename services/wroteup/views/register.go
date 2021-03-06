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

func Register(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("templates/register.html"))

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

		var loginBuf, passwordBuf string

		err = stmt.QueryRow(login).Scan(&loginBuf, &passwordBuf)

		if err == nil {
			http.Error(w, "User already exists", http.StatusForbidden)
			return
		}

		defer stmt.Close()

		tx, err := db.Begin()
		if err != nil {
			http.Error(w, "Can't connect to database", http.StatusInternalServerError)
			return
		}

		stmt, err = tx.Prepare("insert into users (login, password) values(?, ?)")
		if err != nil {
			http.Error(w, "Can't prepare SQL", http.StatusInternalServerError)
			return
		}

		_, err = stmt.Exec(login, password)
		if err != nil {
			http.Error(w, "Can't write data to database", http.StatusInternalServerError)
			return
		}

		tx.Commit()

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
