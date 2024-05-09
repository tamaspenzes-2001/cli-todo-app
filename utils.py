import json
import os

def find_todo_item(selected_todo, todos):
  if selected_todo.startswith("[strike]"):
    selected_todo = selected_todo.strip("[strike]").strip("[/")
  selected_todo = selected_todo.split(" ", 1)[1]
  for todo in todos:
    if todo["text"] == selected_todo:
      return todo

def todos_to_list(todos):
  todos_list = []
  for index, todo in enumerate(todos, start=1):
    if todo["checked"]:
      todos_list.append(f'[strike]{index}. {todo["text"]}[/strike]')
    else:
      todos_list.append(f'{index}. {todo["text"]}')
  return todos_list

def read_todos_from_file():
  with open("todos.json") as todos_doc:
    return json.load(todos_doc)

def save_to_file(todos):
  with open("todos.json", "w") as todos_doc:
    json.dump(todos, todos_doc)

def clear_screen():
  os.system('cls' if os.name=='nt' else 'clear')