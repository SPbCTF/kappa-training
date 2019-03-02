package auth

import (
	"crypto/sha512"
	"errors"
	"fmt"
	"github.com/kappactf/spbctf-20190303/services/wroteup/secrets"
	"net/http"
	"strings"
)

func Authenticate(w http.ResponseWriter, r *http.Request) (string, error) {
	c, err := r.Cookie("KAPPA-AUTH")
	if err != nil {
		return "", err
	}

	buf := strings.SplitN(c.Value, "|", 2)
	login, hash := buf[0], buf[1]

	h := sha512.New384()
	h.Write([]byte(login + secrets.Salt))
	if hash == fmt.Sprintf("%x", h.Sum(nil)) {
		return login, nil
	} else {
		return "", errors.New("auth failed")
	}
}
