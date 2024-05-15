import json
import os
import re
from todo_list import TodoList
from todo_item import TodoItem

def find_todo_item(selected_todo, todos):
  if selected_todo.startswith("[strike]"):
    selected_todo = selected_todo.strip("[strike]").strip("[/")
  selected_todo = selected_todo.split(" ", 1)[1]
  for todo in todos:
    if todo.text == selected_todo:
      return todo

def todos_to_list(todos):
  todos_list = []
  for index, todo in enumerate(todos, start=1):
    if todo.checked:
      todos_list.append(f'[strike]{index}. {todo.text}[/strike]')
    else:
      todos_list.append(f'{index}. {todo.text}')
  return todos_list

def read_todos_from_file(file):
  with open("todos/" + file) as todos_doc:
    todos_data = json.load(todos_doc)
    return process_todos_data(todos_data, file)  

def process_todos_data(data, file):
  list_title = file_name_to_todo_list_name(file)
  todo_list = []
  for todo_data in data:
    todo_list.append(TodoItem(todo_data["text"], todo_data["checked"]))
  return TodoList(list_title, todo_list)

def file_name_to_todo_list_name(file):
  file_name = file.split(".")[0]
  list_title = " ".join(file_name.split("-")).title()
  return list_title

def todo_list_name_to_file_name(list_name):
  file_name = "-".join(re.split(re.compile("\W"), list_name)).lower()
  return file_name + ".json"

def save_to_file(todos, file):
  with open("todos/" + file, "w") as todos_doc:
    json.dump([vars(todo) for todo in todos], todos_doc)

def get_todo_lists():
  if not os.path.isdir("todos"):
    os.makedirs("todos")
  todo_files = os.listdir("todos")
  todo_lists = []
  for file in todo_files:
    list_title = file_name_to_todo_list_name(file)
    todo_lists.append(list_title)
  return todo_lists

def clear_screen():
  os.system('cls' if os.name=='nt' else 'clear')