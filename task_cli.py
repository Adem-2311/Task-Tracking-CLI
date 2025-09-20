import argparse
from utils import add_task, list_tasks, delete_task, update_task_status

parser = argparse.ArgumentParser(
    description='Task Tracker CLI',
    formatter_class=argparse.RawTextHelpFormatter # Allows multiple help text formatting
)

# Subparser to handle multiple commands: add, list, delete, update
subparser = parser.add_subparsers(dest='command', required=True)

# ---------------- add command ----------------
add_parser = subparser.add_parser(
    'add',
    help='Add a new task.',
    description='Add a task with status "Not Done"\n\n\
        Syntax:\n\
            add \"Task description\"\n',
    formatter_class=argparse.RawTextHelpFormatter
)
add_parser.add_argument('description', help='Task description')

# ---------------- list command ----------------
list_parser = subparser.add_parser(
    'list',
    help='List available tasks',
    description='List tasks based on flags.\n\n\
        Syntax:\n\
            list --flag\n\n\
            Valid flags:\n\
                no flag: list all tasks\n\
                --not-done: list all not done tasks\n\
                --in-progress: list all in progress tasks\n\
                --done: list all done tasks\n',
    formatter_class=argparse.RawTextHelpFormatter
)
list_parser.add_argument('--done', action='store_true', help='Show all completed tasks')
list_parser.add_argument('--not-done', action='store_true', help='Show all not done tasks')
list_parser.add_argument('--in-progress', action='store_true', help='Show all in progress tasks')

# ---------------- delete command ----------------
delete_parser = subparser.add_parser(
    'delete',
    help='Delete a task.',
    description='Delete a task based on a given id.\n\n\
        Syntax:\n\
            delete id\n\n\
        To view the specific id for the task, use the list command.\n',
    formatter_class=argparse.RawTextHelpFormatter
)
delete_parser.add_argument('id', type=int, help='ID of the task to delete')

# ---------------- update command ----------------
update_parser = subparser.add_parser(
    'update',
    help="Update a task's status.",
    description="update a task's status based on the task's ID.\n\n\
        Syntax:\n\
            update id --new-status\n\n\
        Valid statuses: --done | --not-done | --in-progress\n\n\
        To view valid ID's, run the list command",
        formatter_class=argparse.RawTextHelpFormatter
)

update_parser.add_argument('id', type=int, help='ID of the task to update')

status_group = update_parser.add_mutually_exclusive_group(required=True)

# Mutually exclusive group → only one status flag can be used at a time
status_group.add_argument('--done', action='store_const', const='Done', dest='status')
status_group.add_argument('--not-done', action='store_const', const='Not Done', dest='status')
status_group.add_argument('--in-progress', action='store_const', const='In Progress', dest='status')

# ---------------- Parse Arguments ----------------
arg = parser.parse_args()

if arg.command == 'add':
    add_task(arg.description)
    
elif arg.command == 'list':
    list_tasks(arg.done, arg.not_done, arg.in_progress)
    
elif arg.command == 'delete':
    delete_task(arg.id)
    
elif arg.command == 'update':
    update_task_status(arg.id, arg.status)