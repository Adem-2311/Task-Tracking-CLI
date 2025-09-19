from datetime import datetime
from enum import Enum
import json
import os

class TaskStatus(Enum):
    DONE = 'Done'
    NOT_DONE = 'Not Done'
    IN_PROGRESS = 'In Progress'

class Task:    
    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.status = TaskStatus.NOT_DONE.value
        self.created_at = datetime.now().isoformat(timespec='milliseconds')
        self.updated_at = datetime.now().isoformat(timespec='milliseconds')
        
    def __str__(self):
        return f'\nTask id: {self.id}\nDescription: {self.description}\nStatus: {self.status}\nCreated at: {self.created_at}\nUpdated at: {self.updated_at}\n\n'

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }
        
    @classmethod
    def from_dict(self, data):
        return self(
            description=data["description"],
            id=data["id"],
            status=data["status"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"]
        )

def load_tasks():
    if not os.path.exists('tasks.json'):
        return []
    
    with open('tasks.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            return []
        
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
    
def add_task(task_des):
    cur_id = 0
    tasks = load_tasks()
    if tasks:
        cur_id = tasks[-1]['id'] + 1
    task = Task(cur_id, task_des)
    tasks.append(task.to_dict())
    save_tasks(tasks)
    
def list_tasks(done = False, not_done = False, in_progress = False):    
    constraints = []
    
    if done:
        constraints.append(TaskStatus.DONE.value)
    if not_done:
        constraints.append(TaskStatus.NOT_DONE.value)
    if in_progress:
        constraints.append(TaskStatus.IN_PROGRESS.value)
    
    if not constraints:
        list_all_tasks()
    else:
        list_with_constraint(constraints)
            
def list_with_constraint(constraints):
    has_displayed = False
    tasks = load_tasks()
                
    if not tasks:
        print('No tasks are saved.')
        return
    
    for task in tasks:
        if task['status'] in constraints:
            print(
                f"\nTask id: {task['id']}\n"
                f"Description: {task['description']}\n"
                f"Status: {task['status']}\n"
                f"Created at: {task['createdAt']}\n"
                f"Updated at: {task['updatedAt']}\n"
            )
            has_displayed = True
            
    if not has_displayed:
        print(f'No tasks were found with the constarints: {[const for const in constraints]}\nTry running list to view lists.')
        
def list_all_tasks():
    tasks = load_tasks()
                
    if not tasks:
        print('No tasks are saved.')
        return
    
    for task in tasks:
        print(
            f"\nTask id: {task['id']}\n"
            f"Description: {task['description']}\n"
            f"Status: {task['status']}\n"
            f"Created at: {task['createdAt']}\n"
            f"Updated at: {task['updatedAt']}\n"
        )
        
def delete_task(task_id):
    tasks = load_tasks()
                
    if not tasks:
        print('There are no tasks to delete.')
        return
    
    if task_id < 0 or task_id not in set(task['id'] for task in tasks):
        print('Invalid ID')
        return
    
    clean = []
    for task in tasks:
        if task['id'] != task_id:
            clean.append(task)
    
    save_tasks(clean)
        
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