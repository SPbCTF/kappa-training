package secrets

import "encoding/hex"

var (
	// CHANGE IT
	Salt         = "KappaSalt"
	CipherKey, _ = hex.DecodeString("6368616e676520746869732070617373776f726420746f206120736563726574")
)
