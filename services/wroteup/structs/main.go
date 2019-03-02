package structs

type Writeup struct {
	Author string
	Ctf string
}

type PageData struct {
	Writeups []Writeup
}
