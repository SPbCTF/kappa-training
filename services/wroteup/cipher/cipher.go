package cipher

import (
	"crypto/aes"
	gocipher "crypto/cipher"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"github.com/kappactf/spbctf-20190303/services/wroteup/secrets"
	"io"
	"log"
	"strings"
)

type BaseCipher struct{}
type SecureCipher struct {
	BaseCipher
}

func (cipher *BaseCipher) Encrypt(data []byte) string {
	s := len(data) % 32
	if s != 0 {
		data = append(data, strings.Repeat("=", 32-s)...)
	}

	return cipher.EncryptData(data)
}

func (cipher *BaseCipher) Decrypt(data string) string {
	return cipher.DecryptData(data)
}

func (cipher *BaseCipher) EncryptData(data []byte) string {
	var result []byte

	for _, c := range data {
		result = append(result, c^'A')
	}

	return fmt.Sprintf("%x", result)
}

func (cipher *BaseCipher) DecryptData(data string) string {
	var result []byte

	dataRaw, _ := hex.DecodeString(data)
	for _, c := range dataRaw {
		result = append(result, c^'A')
	}

	return string(result)
}

func (cipher *SecureCipher) EncryptData(data []byte) string {
	block, err := aes.NewCipher(secrets.CipherKey)
	if err != nil {
		log.Fatal(err)
	}

	nonce := make([]byte, 12)
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		panic(err.Error())
	}

	aesgcm, err := gocipher.NewGCM(block)
	if err != nil {
		panic(err.Error())
	}

	var result = aesgcm.Seal(nil, nonce, data, nil)

	return fmt.Sprintf("%x", nonce) + "|" + fmt.Sprintf("%x", result)
}

func (cipher *SecureCipher) DecryptData(data string) string {
	block, err := aes.NewCipher(secrets.CipherKey)
	if err != nil {
		log.Fatal(err)
	}

	dataArr := strings.SplitN(data, "|", 2)
	nonce, _ := hex.DecodeString(dataArr[0])
	cipherText, _ := hex.DecodeString(dataArr[0])

	aesgcm, err := gocipher.NewGCM(block)
	if err != nil {
		panic(err.Error())
	}

	var result, _ = aesgcm.Open(nil, nonce, cipherText, nil)

	return string(result)
}
