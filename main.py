from beaupy import confirm, prompt, select, select_multiple
from rich.console import Console
import sys

console = Console()

def add_item():
  pass

def choose_todo_action(selected_todo):
  pass

def main():
  console.print("[green underline]YOUR TODOS:[/green underline]")
  while True:
    todos = []
    with open("todos.txt") as todos_doc:
      for todo in todos_doc:
        todos.append(todo.strip())
    todos.append("[cyan]Add item[/cyan]")
    todos.append("[red]Quit[/red]")
    # print("\n\x1b[92mCOMMANDS:\x1b[0m")
    # print("add [todo text]: add a todo")
    # print("quit: quit app")
    # user_choice = input("> ")
    selected_todo = select(todos)
    match selected_todo:
      case "[cyan]Add item[/cyan]": add_item()
      case "[red]Quit[/red]":
        if confirm("Are you sure you want to quit?"):
          sys.exit()
      case _: choose_todo_action(selected_todo)

main()