import argparse
from utils import add_task, list_tasks, delete_task, update_task_status

parser = argparse.ArgumentParser(description='Task Tracker CLI')
subparser = parser.add_subparsers(dest='command', required=True)

# Adding add command
add_parser = subparser.add_parser(
    'add',
    help='Add task with status "Not Done"\n syntax: add "description"'
)
add_parser.add_argument('description', help='Task description')

# Adding list command
list_parser = subparser.add_parser(
    'list',
    help='List Tasks based on flags.\n syntax: list --flag \
    --flag:\n\
    none: list all tasks\n\
    --not-done: list all not done tasks\n\
    --in-progress: list all in progres tasks\n\
    --done: list all done tasks\n'
)
list_parser.add_argument('--done', action='store_true', help='Show all completed tasks')
list_parser.add_argument('--not-done', action='store_true', help='Show all not done tasks')
list_parser.add_argument('--in-progress', action='store_true', help='Show all in progress tasks')

# Adding delete command
delete_parser = subparser.add_parser(
    'delete',
    help='Delete a task based on a given id.\n\
    syntax: delete id\n\
    to view the specific id for the task, use the list command.\n'
)
delete_parser.add_argument('id', type=int, help='ID of the task to delete')

# Adding update command
update_parser = subparser.add_parser(
    'update',
    help="update a task's status based on the task's ID.\n\
    syntax: update id --new-status\n\
    Valid statuses: Done | Not Done | In Progress\n\
    To view valid ID's, please run the list command"
)

update_parser.add_argument('id', type=int, help='ID of the task to update')

status_group = update_parser.add_mutually_exclusive_group(required=True)
status_group.add_argument('--done', action='store_const', const='Done', dest='status')
status_group.add_argument('--not-done', action='store_const', const='Not Done', dest='status')
status_group.add_argument('--in-progress', action='store_const', const='In Progress', dest='status')
arg = parser.parse_args()

if arg.command == 'add':
    add_task(arg.description)
    
elif arg.command == 'list':
    list_tasks(arg.done, arg.not_done, arg.in_progress)
    
elif arg.command == 'delete':
    delete_task(arg.id)
    
elif arg.command == 'update':
    update_task_status(arg.id, arg.status)
    
else:
    print('Invaid command')