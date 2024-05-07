from beaupy import confirm, prompt, select, select_multiple
from rich.console import Console
import sys
import os

console = Console()

def add_item():
  new_item = ""
  while new_item == "":
    new_item = prompt("New item:").strip()
  with open("todos.txt", "a") as todos_doc:
    todos_doc.write("\n" + new_item)

def remove_item(selected_todo, todos):
  if confirm(f'Delete item "{selected_todo}" from the list?'):
    todos.remove(selected_todo.split(" ", 1)[1])
    with open("todos.txt", "w") as todos_doc:
      for todo in todos[:-2]:
        todos_doc.write("\n" + todo)

def main():
  while True:
    os.system('cls' if os.name=='nt' else 'clear')
    console.print("[green underline]YOUR TODOS:[/green underline]")
    todos = []
    with open("todos.txt") as todos_doc:
      for todo in todos_doc:
        if todo.strip() != "":
          todos.append(todo.strip())
    todos.append("[cyan]Add item[/cyan]")
    todos.append("[red]Quit[/red]")
    selected_todo = select([str(index) + ". " + todo for index, todo in enumerate(todos[:-2], start=1)] + todos[-2:])
    # Keep select items visible after selecting an option
    for todo in todos[:-2]:
      print(todo)
    match selected_todo:
      case "[cyan]Add item[/cyan]": add_item()
      case "[red]Quit[/red]":
        if confirm("Are you sure you want to quit?"):
          sys.exit()
      case _: remove_item(selected_todo, todos)

main()