package views

import (
	"fmt"
	"github.com/kappactf/spbctf-20190303/services/wroteup/auth"
	"github.com/kappactf/spbctf-20190303/services/wroteup/cipher"
	"github.com/kappactf/spbctf-20190303/services/wroteup/database"
	"log"
	"net/http"
)

func ShowWriteup(w http.ResponseWriter, r *http.Request) {

	if r.Method == "GET" {
		login, err := auth.Authenticate(w, r)
		if err != nil {
			http.Error(w, "Auth failed", http.StatusForbidden)
			return
		}

		r.ParseForm()

		ctf := r.Form.Get("ctf")

		db := database.Get()

		stmt, err := db.Prepare("select author, writeup from writeups where ctf = ?")
		if err != nil {
			log.Fatal(err)
		}

		defer stmt.Close()
		var writeup string
		var author string
		err = stmt.QueryRow(ctf).Scan(&author, &writeup)
		if err != nil {
			log.Fatal(err)
		}

		c := cipher.SecureCipher{}

		if author == login {
			fmt.Fprintln(w, c.Decrypt(writeup))
		} else {
			fmt.Fprintln(w, writeup)
		}

	} else {
		fmt.Fprintln(w, "Unsupported method")
	}
}
