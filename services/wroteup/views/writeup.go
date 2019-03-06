package views

import (
	"fmt"
	"github.com/kappactf/spbctf-20190303/services/wroteup/auth"
	"github.com/kappactf/spbctf-20190303/services/wroteup/cipher"
	"github.com/kappactf/spbctf-20190303/services/wroteup/database"
	"net/http"
)

func PostWriteup(w http.ResponseWriter, r *http.Request) {

	if r.Method == "POST" {
		login, err := auth.Authenticate(w, r)
		if err != nil {
			http.Error(w, "Auth failed", http.StatusForbidden)
			return
		}

		err = r.ParseForm()
		if err != nil {
			http.Error(w, "Can't parse form", http.StatusInternalServerError)
			return
		}

		ctf := r.Form.Get("ctf")
		writeup := r.Form.Get("writeup")

		db := database.Get()

		tx, err := db.Begin()
		if err != nil {
			http.Error(w, "Can't connect to database", http.StatusInternalServerError)
			return
		}

		stmt, err := tx.Prepare("insert into writeups (author, ctf, writeup) values(?, ?, ?)")
		if err != nil {
			http.Error(w, "Can't prepare SQL", http.StatusInternalServerError)
			return
		}

		c := cipher.SecureCipher{}

		_, err = stmt.Exec(login, ctf, c.Encrypt([]byte(writeup)))
		if err != nil {
			http.Error(w, "Can't write to database", http.StatusInternalServerError)
			return
		}

		err = tx.Commit()
		if err != nil {
			http.Error(w, "Can't commit to database", http.StatusInternalServerError)
			return
		}

		if _, err = fmt.Fprintln(w, "Success"); err != nil {
			http.Error(w, "Can't send response", http.StatusInternalServerError)
			return
		}

	} else {
		if _, err := fmt.Fprintln(w, "Unsupported method"); err != nil {
			http.Error(w, "Can't send response", http.StatusInternalServerError)
			return
		}
	}
}
