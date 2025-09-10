from datetime import datetime
from enum import Enum
import json
import os

class TaskStatus(Enum):
    DONE = 'Done'
    NOT_DONE = 'Not Done'
    IN_PROGRESS = 'In Progress'

class Task:
    cur_id = 0
    
    def __init__(self, description):
        Task.cur_id += 1
        self.id = Task.cur_id
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
        
    '''
    @classmethod
    def from_dict(cls, data):
        return cls(
            description=data["description"],
            id=data["id"],
            status=data["status"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"]
        )
    '''
        
def load_tasks():
    if not os.path.exists('tasks.json'):
        return []
    
    with open('tasks.json') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(e)
            return []
        
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
            
def set_max_id():
    tasks = load_tasks()
    Task.cur_id = max([task['id'] for task in tasks], default=0)
    
def add_task(task):
    tasks = load_tasks()
    tasks.append(task.to_dict())
    save_tasks(tasks)
    set_max_id()
        
def clean_duplicates():
    tasks = load_tasks()
                
    if not tasks:
        return
                
    seen = set()
    cleaned = []
    
    for task in tasks:
        if task['id'] not in seen:
            cleaned.append(task)
            seen.add(task['id'])
            
    save_tasks(cleaned)        
    set_max_id()
        
def update_task(task_id, new_description = None, new_status = None):
    tasks = load_tasks()
                
    if not tasks:
        print('No tasks to update')
        return
                
    for task in tasks:
        if task['id'] == task_id:
            if new_description:
                task['description'] = new_description
            if new_status and new_status in [status.value for status in TaskStatus]:
                task['status'] = new_status
                
            task['updatedAt'] = datetime.now().isoformat(timespec='milliseconds')
            break
        
    save_tasks(tasks)
        
def delete_task(task_id):
    tasks = load_tasks()
                
    if not tasks:
        print('There are no tasks to delete.')
        return
                
    tasks = [task for task in tasks if task['id'] != task_id]
    
    save_tasks(tasks)        
    set_max_id()
        
def list_all_tasks(constraint = None):
    tasks = load_tasks()
                
    if not tasks:
        print('No tasks are saved.')
        return
    
    for task in tasks:
        #  task = Task.from_dict(task_dict)
        if not constraint or task['status'] == constraint:
            print(task.__str__)