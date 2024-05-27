import os
import sys
from rich.console import Console
from todo_item import TodoItem

console = Console()

def find_todo_item(selected_todo, todos):
  for todo in todos:
    if todo.text == selected_todo:
      return todo

def strip_todo_decoration(todo):
  if todo.startswith("[strike]"):
    todo = todo.strip("[strike]").strip("[/")
  todo = todo.split(" ", 1)[1]
  return todo

def todos_to_list(app, todo_list):
  todos = []
  for i, item in enumerate(todo_list, start=1):
    todo = ""
    if item.checked:
      todo += (f'[strike]{i}. {item.text}[/strike]')
    else:
      todo += (f'{i}. {item.text}')
    j = 1
    for subitem in item.items:
      if not subitem.checked:
        todo += (f'\n    {j}. {subitem.text}')
        j += 1
      elif app.show_checked:
        todo += (f'\n    [strike]{j}. {subitem.text}[/strike]')
        j += 1
    todos.append(todo)
  return todos

def get_todos_to_show(app, todo_list):
  if app.show_checked:
    return todos_to_list(todo_list.items, app)
  else:
    return todos_to_list([todo for todo in todo_list.items if not todo.checked], app)

def print_todos(todos):
  for todo in todos:
    console.print(todo)

def is_list_name_valid(list_name):
  longer_than_zero = len(list_name) > 0
  no_invalid_chars = all(char not in list_name for char in (".", "/"))
  return longer_than_zero and no_invalid_chars

def clear_screen():
  os.system('cls' if os.name=='nt' else 'clear')

def restart_program():
  os.execl(sys.executable, sys.executable, *sys.argv)