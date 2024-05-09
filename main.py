from beaupy import confirm, prompt, select, select_multiple
from rich.console import Console
import sys
import os
import json

console = Console()

def add_item(todos):
  new_item = ""
  while new_item == "":
    new_item = prompt("New item:").strip()
  todos.append({"text": new_item, "checked": False})
  with open("todos.json", "w") as todos_doc:
    json.dump(todos, todos_doc)

def check_item(selected_todo, todos):
  pass

def edit_item(selected_todo, todos):
  pass

def remove_item(selected_todo, todos):
  if confirm(f'Delete item "{selected_todo}" from the list?'):
    selected_todo = find_todo_item(selected_todo, todos)
    todos.remove(selected_todo)
    with open("todos.json", "w") as todos_doc:
      json.dump(todos, todos_doc)

def move_item_up(selected_todo, todos):
  pass

def move_item_down(selected_todo, todos):
  pass

def todo_options_menu(selected_todo, todos):
  console.print(f"[cyan]Selected: {selected_todo}[/cyan]")
  options = ["1. Check", "2. Edit", "3. Delete", "4. Move up", "5. Move down"]
  operation = select(options, return_index=True)
  match operation:
    case 0: check_item(selected_todo, todos)
    case 1: edit_item(selected_todo, todos)
    case 2: remove_item(selected_todo, todos)
    case 3: move_item_up(selected_todo, todos)
    case 4: move_item_down(selected_todo, todos)

def find_todo_item(selected_todo, todos):
  selected_todo = selected_todo.split(" ", 1)[1]
  for todo in todos:
    if todo["text"] == selected_todo:
      return todo

def todos_to_list(todos):
  todos_list = []
  for index, todo in enumerate(todos, start=1):
    todos_list.append(str(index) + ". " + todo["text"])
  return todos_list

def main():
  while True:
    os.system('cls' if os.name=='nt' else 'clear')
    console.print("[green underline]YOUR TODOS:[/green underline]")
    with open("todos.json") as todos_doc:
      todos = json.load(todos_doc)
    options = todos_to_list(todos) + ["[cyan]Add item[/cyan]", "[red]Quit[/red]"]
    selected_todo = select(options)
    # Keep todo items visible after selecting an option
    for todo in todos_to_list(todos):
      print(todo)
    match selected_todo:
      case "[cyan]Add item[/cyan]": add_item(todos)
      case "[red]Quit[/red]":
        if confirm("Are you sure you want to quit?"):
          sys.exit()
      case _: todo_options_menu(selected_todo, todos)

main()