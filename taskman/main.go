package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	db, err := sql.Open("sqlite3", "./tasks.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	_, err = db.Exec(`
		CREATE TABLE IF NOT EXISTS tasks (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL,
			done BOOLEAN DEFAULT 0,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)
	`)
	if err != nil {
		log.Fatal(err)
	}
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <command> [args]")
		return
	}
	var arg = os.Args[1]
	if arg == "add" {
		if len(os.Args) < 3 {
			fmt.Println("Usage: go run main.go add <task>")
			return
		}
		var task = os.Args[2]
		if task != "" {
			_, err = db.Exec("INSERT INTO tasks (title) VALUES (?)", task)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Println("Task added successfully")
		}

	}

}
