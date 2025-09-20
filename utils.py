from datetime import datetime
from enum import Enum
import json
import os

# Enum class to represent possible task statuses
class TaskStatus(Enum):
    DONE = 'Done'
    NOT_DONE = 'Not Done'
    IN_PROGRESS = 'In Progress'

# Represents a single task
class Task:    
    def __init__(self, id, description, status=TaskStatus.NOT_DONE.value, created_at=None, updated_at=None):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now().isoformat(timespec='milliseconds')
        self.updated_at = updated_at or datetime.now().isoformat(timespec='milliseconds')
        
    # How the task will look when printed
    def __str__(self):
        return (
            f'\nTask id: {self.id}\n'
            f'Description: {self.description}\n'
            f'Status: {self.status}\n'
            f'{self.format_date()}'
        )

    # Convert Task object into dictionary (for JSON storage)
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }
        
    # Format date nicely for display
    def format_date(self):
        create_date = self.created_at.split('T')
        update_date = self.updated_at.split('T')
        
        return (
            f'Created at: {create_date[0]} at {create_date[1]}\n'
            f'Updated at: {update_date[0]} at {update_date[1]}\n'
        )
    
    # Create a Task object back from dictionarydata (reverse of to_dict)
    @classmethod
    def from_dict(self, data):
        return self(
            description=data["description"],
            id=data["id"],
            status=data["status"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"]
        )

# Load all tasks from JSON file
def load_tasks():
    if not os.path.exists('tasks.json'):
        return []
    
    with open('tasks.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            return []
      
# Save all tasks back to JSON file  
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
    
# Add a new task with a unique ID
def add_task(task_des):
    cur_id = 0
    tasks = load_tasks()
    if tasks:
        cur_id = tasks[-1]['id'] + 1
    task = Task(cur_id, task_des)
    tasks.append(task.to_dict())
    save_tasks(tasks)
   
# List tasks based on filter flags 
def list_tasks(done = False, not_done = False, in_progress = False):    
    constraints = set()
    
    if done:
        constraints.add(TaskStatus.DONE.value)
    if not_done:
        constraints.add(TaskStatus.NOT_DONE.value)
    if in_progress:
        constraints.add(TaskStatus.IN_PROGRESS.value)
    
    # If no filters applied, then list everything
    if not constraints:
        list_all_tasks()
    else:
        list_with_constraint(constraints)
            
# List only tasks that match the given constraints
def list_with_constraint(constraints):
    has_displayed = False
    tasks = load_tasks()
                
    if not tasks:
        print('No tasks are saved.')
        return
    
    for task_dict in tasks:
        if task_dict['status'] in constraints:
            task = Task.from_dict(task_dict)
            print(task)
            has_displayed = True
            
    if not has_displayed:
        print(f'No tasks were found with the constarints: {[const for const in constraints]}\nTry running list to view lists.')
     
# List all tasks (ignores constraints)   
def list_all_tasks():
    tasks = load_tasks()
                
    if not tasks:
        print('No tasks are saved.')
        return
    
    for task_dict in tasks:
        task = Task.from_dict(task_dict)
        print(task)
        
# Delete a task by its ID
def delete_task(task_id):
    tasks = load_tasks()
                
    if not tasks:
        print('There are no tasks to delete.')
        return
    
    if task_id < 0 or task_id not in set(task['id'] for task in tasks):
        print('Invalid ID')
        return
    
    # Keep only tasks that are not the one we want to delete
    clean = [task for task in tasks if task['id'] != task_id]
    
    save_tasks(clean)
     
# Update the status of a task by ID   
def update_task_status(task_id, new_status = None):
    if not new_status or new_status not in [status.value for status in TaskStatus]:
        print('Invalid status arguments')
        return
    
    tasks = load_tasks()
    
    if task_id < 0 or task_id not in set(task['id'] for task in tasks):
        print('Invalid ID')
        return
                
    if not tasks:
        print('No tasks to update')
        return
    
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status    
            task['updatedAt'] = datetime.now().isoformat(timespec='milliseconds')
            break
        
    save_tasks(tasks)