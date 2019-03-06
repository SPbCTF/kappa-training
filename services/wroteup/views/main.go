package views

import (
	"github.com/kappactf/spbctf-20190303/services/wroteup/auth"
	"github.com/kappactf/spbctf-20190303/services/wroteup/database"
	"github.com/kappactf/spbctf-20190303/services/wroteup/structs"
	"html/template"
	"net/http"
)

func Main(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("templates/main.html"))
	wr := structs.PageData{}

	_, err := auth.Authenticate(w, r)
	if err != nil {
		http.Error(w, "Auth failed", http.StatusForbidden)
		return
	}

	db := database.Get()

	rows, err := db.Query("select ctf, author from writeups order by time desc limit 30")

	for rows.Next() {
		var ctf string
		var author string
		err = rows.Scan(&ctf, &author)
		if err != nil {
			http.Error(w, "Can't scan from database", http.StatusInternalServerError)
			return
		}
		wr.Writeups = append(wr.Writeups, structs.Writeup{
			Author: author,
			Ctf:    ctf,
		})
	}
	err = rows.Err()
	if err != nil {
		http.Error(w, "Unknown error", http.StatusInternalServerError)
		return
	}

	if err := tmpl.Execute(w, wr); err != nil {
		http.Error(w, "Can't produce template", http.StatusInternalServerError)
		return
	}
}
