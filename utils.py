import json
import os
import re
import sys
from todo_list import TodoList
from todo_item import TodoItem
from rich.console import Console

console = Console()

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

def print_todos(todos):
  for todo in todos:
    console.print(todo)

def read_todos_from_file(list_name):
  with open(f"todos/{list_name}.json") as todos_doc:
    todos_data = json.load(todos_doc)
    return process_todos_data(todos_data, list_name)

def rename_file(list_name, new_list_name):
  os.rename(f"todos/{list_name}.json", f"todos/{new_list_name}.json")

def delete_file(list_name):
  os.remove(f"todos/{list_name}.json")

def process_todos_data(data, file):
  todo_list = []
  for todo_data in data:
    todo_list.append(TodoItem(todo_data["text"], todo_data["checked"]))
  return TodoList(file.split(".")[0], todo_list)

def is_list_name_valid(list_name):
  longer_than_zero = len(list_name) > 0
  no_invalid_chars = all(char not in list_name for char in (".", "/"))
  return longer_than_zero and no_invalid_chars

def save_to_file(todos, list_name):
  with open(f"todos/{list_name}.json", "w") as todos_doc:
    json.dump([vars(todo) for todo in todos], todos_doc)

def get_todo_lists():
  if not os.path.isdir("todos"):
    os.makedirs("todos")
  todo_files = os.listdir("todos")
  todo_lists = []
  for file in todo_files:
    todo_lists.append(file.split(".")[0])
  todo_lists.sort()
  return todo_lists

def clear_screen():
  os.system('cls' if os.name=='nt' else 'clear')

def restart_program():
  os.execl(sys.executable, sys.executable, *sys.argv)