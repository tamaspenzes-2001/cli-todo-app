from beaupy import confirm, prompt, select, select_multiple
from rich.console import Console
import sys
import utils

console = Console()

def add_item(todos):
  new_item = ""
  while new_item == "":
    new_item = prompt("New item:").strip()
  todos.append({"text": new_item, "checked": False})
  utils.save_to_file(todos)

def toggle_check_item(selected_todo):
  if selected_todo["checked"]:
    selected_todo["checked"] = False
  else:
    selected_todo["checked"] = True

def edit_item(selected_todo):
  modified_todo_text = ""
  while modified_todo_text == "":
    modified_todo_text = prompt("Edit todo:", initial_value=selected_todo["text"]).strip()
  selected_todo["text"] = modified_todo_text

def remove_item(selected_todo, todos):
  if confirm(f'Delete item from the list?'):
    todos.remove(selected_todo)

def move_item_up(selected_todo, todos):
  pass

def move_item_down(selected_todo, todos):
  pass

def todo_options_menu(selected_todo, todos):
  console.print(f"[cyan]Selected: {selected_todo}[/cyan]")
  options = ["1. Toggle check", "2. Edit", "3. Delete", "4. Move up", "5. Move down"]
  operation = select(options, return_index=True)
  selected_todo = utils.find_todo_item(selected_todo, todos)
  match operation:
    case 0: toggle_check_item(selected_todo)
    case 1: edit_item(selected_todo)
    case 2: remove_item(selected_todo, todos)
    case 3: move_item_up(selected_todo, todos)
    case 4: move_item_down(selected_todo, todos)
  utils.save_to_file(todos)

def main():
  todos = utils.read_todos_from_file()
  show_checked = False
  while True:
    utils.clear_screen()
    console.print("[green underline]YOUR TODOS:[/green underline]")
    if show_checked:
      todos_list = utils.todos_to_list(todos)
    else:
      todos_list = utils.todos_to_list([todo for todo in todos if not todo["checked"]])
    add_item_option = "[cyan]Add item[/cyan]"
    show_hide_option = f"{'Hide' if show_checked else 'Show'} checked items"
    quit_option = "[red]Quit[/red]"
    options = todos_list + [add_item_option, show_hide_option, quit_option]
    selected = select(options)
    # Keep todo items visible after selecting an option
    for todo in todos_list:
      console.print(todo)

    if selected == add_item_option:
      add_item(todos)
    elif selected == show_hide_option:
      show_checked = not show_checked
    elif selected == quit_option:
      if confirm("Are you sure you want to quit?"):
        sys.exit()
    else:
      todo_options_menu(selected, todos)

main()