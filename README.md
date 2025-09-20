# 📌 Task Tracking CLI App 📝

project page url [here](https://roadmap.sh/projects/task-tracker)

## 📖 Description

A simple command-line task manager written in Python.
It lets you add, update, delete and list tasks, all saved in a JSON file.

## ⚡ Features

- Add new tasks with a description.
- Mark tasks as **Done**, **Not Done** or **In Progress**.
- List tasks with filters (`--done`, `--not-done`, `--in-progress`).
- Delete tasks by ID.
- Prevent duplicate tasks IDs automatically.

## 🔧 Installation

### Install Python

You can install Python from the official website [here](https://www.python.org/downloads/)

### Clone the repo

```cdm
git clone https://github.com/Adem-2311/Task-Tracking-CLI
cd task-tracker-cli
```

## 🚀 Usage

### Run the CLI:

```cmd
python task_cli.py <command> [options]
```

#### Commands

- **Add a task**

```cmd
python task_cli.py add "Buy groceries"
```

- **List all tasks**

```cmd
python task_cli.py list
```

- **List tasks by status**

```cmd
python task_cli.py list --done
python task_cli.py list --in-progress
python task_cli.py list --not-done
```

- **Update a task**

```cmd
python task_cli.py update 2 --done
python task_cli.py update 5 --in-progress
```

- **Delete a task**

```cmd
python task_cli.py delete 3
```