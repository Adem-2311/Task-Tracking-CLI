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
        
def save_task(task):
    tasks = []
        
    # Read existing tasks if they exist
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            try:
                tasks = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(e)
                    
    # Append the new task
    tasks.append(task.to_dict())
        
    # Write to the file
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
            
    if tasks:
        Task.cur_id = tasks[-1]['id']
    else:
        Task.cur_id = 0
        
def clean_duplicates():
    tasks = []
    
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            try:
                tasks = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(e)
                
    if len(tasks) == 0:
        return
                
    seen = set()
    cleaned = []
    
    for task in tasks:
        if task['id'] not in seen:
            cleaned.append(task)
            seen.add(task['id'])
            
    with open('tasks.json', 'w') as f:
        json.dump(cleaned, f, indent=4)
        
def update_task(task_id, new_description = None, new_status = None):
    tasks = []
    
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            try:
                tasks = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(e)
                
    if len(tasks) == 0:
        print('No tasks to update')
        return
                
    for task in tasks:
        if task['id'] == task_id:
            if new_description:
                task['description'] = new_description
            if new_status:
                task['status'] = new_status
                
            task['updatedAt'] = datetime.now().isoformat(timespec='milliseconds')
            
            break
        
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
        
def delete_task(task_id):
    tasks = []
    
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            try:
                tasks = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(e)
                
    if len(tasks) == 0:
        print('There are no tasks to delete.')
        return
                
    tasks = [task for task in tasks if task['id'] != task_id]
    
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
        
def list_all_tasks(constraint = None):
    tasks = []
    
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            try:
                tasks = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(e)
                
    if len(tasks) == 0:
        print('No tasks are saved.')
        return
    
    for task in tasks:
        if not constraint:
            print(task)
        elif task['status'] == constraint:
            print(task)

t1 = Task('fat task')
t2 = Task('big hard task')
t3 = Task('monkey task')