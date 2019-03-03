package views

import (
	"fmt"
	"github.com/kappactf/spbctf-20190303/services/wroteup/auth"
	"github.com/kappactf/spbctf-20190303/services/wroteup/cipher"
	"github.com/kappactf/spbctf-20190303/services/wroteup/database"
	"net/http"
)

func ShowWriteup(w http.ResponseWriter, r *http.Request) {

	if r.Method == "GET" {
		login, err := auth.Authenticate(w, r)
		if err != nil {
			http.Error(w, "Auth failed", http.StatusForbidden)
			return
		}

		if err := r.ParseForm(); err != nil {
			http.Error(w, "Can't parse form", http.StatusInternalServerError)
			return
		}

		ctf := r.Form.Get("ctf")

		db := database.Get()

		stmt, err := db.Prepare("select author, writeup from writeups where ctf = ?")
		if err != nil {
			http.Error(w, "Can't prepare SQL", http.StatusInternalServerError)
			return
		}

		defer stmt.Close()
		var writeup string
		var author string
		err = stmt.QueryRow(ctf).Scan(&author, &writeup)
		if err != nil {
			http.Error(w, "Can't scan from database", http.StatusInternalServerError)
			return
		}

		c := cipher.SecureCipher{}

		if author == login {
			if _, err := fmt.Fprintln(w, c.Decrypt(writeup)); err != nil {
				http.Error(w, "Can't response", http.StatusInternalServerError)
				return
			}
		} else {
			if _, err := fmt.Fprintln(w, writeup); err != nil {
				http.Error(w, "Can't response", http.StatusInternalServerError)
				return
			}
		}

	} else {
		if _, err := fmt.Fprintln(w, "Unsupported method"); err != nil {
			http.Error(w, "Can't response", http.StatusInternalServerError)
			return
		}
	}
}
