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

def choose_todo_action(selected_todo):
  pass

def main():
  while True:
    os.system('cls' if os.name=='nt' else 'clear')
    console.print("[green underline]YOUR TODOS:[/green underline]")
    todos = []
    with open("todos.txt") as todos_doc:
      for index, todo in enumerate(todos_doc, start=1):
        todos.append(str(index) + ". " + todo.strip())
    todos.append("[cyan]Add item[/cyan]")
    todos.append("[red]Quit[/red]")
    selected_todo = select(todos)
    # Keep select items visible after selecting an option
    for todo in todos[:-2]:
      print(todo)
    match selected_todo:
      case "[cyan]Add item[/cyan]": add_item()
      case "[red]Quit[/red]":
        if confirm("Are you sure you want to quit?"):
          sys.exit()
      case _: choose_todo_action(selected_todo)

main()