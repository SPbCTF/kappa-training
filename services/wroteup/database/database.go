package database

import (
	"database/sql"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
)

var (
	database *sql.DB
)

func init() {
	db, err := sql.Open("sqlite3", "./db.db")
	if err != nil {
		fmt.Println("Can't open database", err.Error())
	}

	database = db
}

func Get() *sql.DB {
	return database
}
