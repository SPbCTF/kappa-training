package views

import (
	"fmt"
	"github.com/kappactf/spbctf-20190303/services/wroteup/auth"
	"github.com/kappactf/spbctf-20190303/services/wroteup/cipher"
	"github.com/kappactf/spbctf-20190303/services/wroteup/database"
	"log"
	"net/http"
)

func PostWriteup(w http.ResponseWriter, r *http.Request) {

	if r.Method == "POST" {
		login, err := auth.Authenticate(w, r)
		if err != nil {
			http.Error(w, "Auth failed", http.StatusForbidden)
			return
		}

		r.ParseForm()

		ctf := r.Form.Get("ctf")
		writeup := r.Form.Get("writeup")

		db := database.Get()

		tx, err := db.Begin()
		if err != nil {
			log.Fatal(err)
		}

		stmt, err := tx.Prepare("insert into writeups (author, ctf, writeup) values(?, ?, ?)")
		if err != nil {
			log.Fatal(err)
		}

		c := cipher.SecureCipher{}

		_, err = stmt.Exec(login, ctf, c.Encrypt([]byte(writeup)))
		if err != nil {
			log.Fatal(err)
		}

		tx.Commit()

		fmt.Fprintln(w, "Success")

	} else {
		fmt.Fprintln(w, "Unsupported method")
	}
}
