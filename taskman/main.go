package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	"strconv"

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

	switch arg {
	case "add":
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
	case "done":
		if len(os.Args) < 3 {
			log.Fatal("Command usage done <id>")
		}
		var stringVlaue string = os.Args[2]
		id, err := strconv.Atoi(stringVlaue)
		if err != nil {
			log.Fatal(err)
		}
		_, err = db.Exec("UPDATE tasks SET done =1 WHERE id=?", id)
		if err != nil {
			log.Fatal(err)
		}

	case "delete":
		if len(os.Args) < 3 {
			log.Fatal("Command usage done <id>")
		}
		var stringVlaue string = os.Args[2]
		id, err := strconv.Atoi(stringVlaue)
		if err != nil {
			log.Fatal(err)
		}
		_, err = db.Exec("DELETE FROM tasks WHERE id=?", id)
		if err != nil {
			log.Fatal(err)
		}

	case "list":
		rows, err := db.Query("select * from tasks")
		if err != nil {
			log.Fatal(err)
		}
		defer rows.Close()

		for rows.Next() {
			var id int
			var title string
			var done bool
			var created_at string
			if err := rows.Scan(&id, &title, &done, &created_at); err != nil {
				log.Fatal(err)
			}
			fmt.Println(id, title, done, created_at)
		}

	}
	// if arg == "add" {
	// 	if len(os.Args) < 3 {
	// 		fmt.Println("Usage: go run main.go add <task>")
	// 		return
	// 	}
	// 	var task = os.Args[2]
	// 	if task != "" {
	// 		_, err = db.Exec("INSERT INTO tasks (title) VALUES (?)", task)
	// 		if err != nil {
	// 			log.Fatal(err)
	// 		}
	// 		fmt.Println("Task added successfully")
	// 	}

	// } else if arg == "list" {
	// 	rows, err := db.Query("select * from tasks")
	// 	if err != nil {
	// 		log.Fatal(err)
	// 	}
	// 	defer rows.Close()

	// 	for rows.Next() {
	// 		var id int
	// 		var title string
	// 		var done bool
	// 		var created_at string
	// 		if err := rows.Scan(&id, &title, &done, &created_at); err != nil {
	// 			log.Fatal(err)
	// 		}
	// 		fmt.Println(id, title, done, created_at)
	// 	}

	// } else if arg == "done" {

	// 	if len(os.Args) < 3 {
	// 		log.Fatal("Command usage done <id>")
	// 	}
	// 	var stringVlaue string = os.Args[2]
	// 	id, err := strconv.Atoi(stringVlaue)
	// 	if err != nil {
	// 		log.Fatal(err)
	// 	}
	// 	_, err = db.Exec("UPDATE tasks SET done =1 WHERE id=?", id)
	// 	if err != nil {
	// 		log.Fatal(err)
	// 	}

	// } else if arg == "delete" {

	// 	if len(os.Args) < 3 {
	// 		log.Fatal("Command usage done <id>")
	// 	}
	// 	var stringVlaue string = os.Args[2]
	// 	id, err := strconv.Atoi(stringVlaue)
	// 	if err != nil {
	// 		log.Fatal(err)
	// 	}
	// 	_, err = db.Exec("DELETE FROM tasks WHERE id=?", id)
	// 	if err != nil {
	// 		log.Fatal(err)
	// 	}

	// }

}
