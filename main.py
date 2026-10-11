import sqlite3


class TaskManager:
    def __init__(self):
        self.connection = sqlite3.connect("tasks.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'Medium',
                deadline TEXT,
                status TEXT DEFAULT 'Pending'
            )
        """)
        self.connection.commit()

    def add_task(self):
        title = input("Enter task title: ").strip()

        if not title:
            print("Task title cannot be empty!")
            return

        description = input("Enter task description: ").strip()
        priority = input("Enter priority (Low/Medium/High): ").strip().capitalize()

        if priority not in ["Low", "Medium", "High"]:
            print("Invalid priority! Using Medium.")
            priority = "Medium"

        deadline = input("Enter deadline (YYYY-MM-DD): ").strip()

        self.cursor.execute("""
            INSERT INTO tasks (title, description, priority, deadline)
            VALUES (?, ?, ?, ?)
        """, (title, description, priority, deadline))

        self.connection.commit()
        print("Task added successfully!")

    def view_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()

        if not tasks:
            print("No tasks found.")
            return

        print("\n========== YOUR TASKS ==========")

        for task in tasks:
            print(f"\nID: {task[0]}")
            print(f"Title: {task[1]}")
            print(f"Description: {task[2]}")
            print(f"Priority: {task[3]}")
            print(f"Deadline: {task[4] or 'Not set'}")
            print(f"Status: {task[5]}")

    def close(self):
        self.connection.close()


manager = TaskManager()

while True:
    print("\n===== SMART TASK MANAGER =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        manager.add_task()
    elif choice == "2":
        manager.view_tasks()
    elif choice == "3":
        manager.close()
        print("Goodbye!")
        break
    else:
        print("Invalid choice! Try again.")