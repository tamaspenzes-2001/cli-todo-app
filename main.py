from beaupy import confirm, select
from rich.console import Console
import sys
import utils
from todo_app import TodoApp

console = Console()

def todo_options_menu(selected_todo, todo_list):
  console.print(f"[cyan]Selected: {selected_todo}[/cyan]")
  options = ["1. Toggle check", "2. Edit", "3. Delete", "4. Move up", "5. Move down"]
  operation = select(options, return_index=True)
  selected_todo = utils.find_todo_item(selected_todo, todo_list.todos)
  match operation:
    case 0: selected_todo.toggle_checked()
    case 1: selected_todo.edit_text()
    case 2: todo_list.remove_item(selected_todo)
    case 3: todo_list.move_item_up(selected_todo)
    case 4: todo_list.move_item_down(selected_todo)
  file_name = utils.todo_list_name_to_file_name(todo_list.title)
  utils.save_to_file(todo_list.todos, file_name)

def choose_todo_list(app):
  while True:
    utils.clear_screen()
    console.print("[green underline]TODO LISTS[/green underline]")
    create_list_option = "[cyan]Create new list[/cyan]"
    options = app.todo_lists + [create_list_option]
    user_selection = select(options)
    if user_selection == create_list_option:
      app.create_list()
    else:
      todo_list = next((todo_list for todo_list in app.loaded_todo_lists if todo_list.title == user_selection), None)
      if todo_list is None:
        file_name = utils.todo_list_name_to_file_name(user_selection)
        todo_list = utils.read_todos_from_file(file_name)
        app.loaded_todo_lists.append(todo_list)
      return todo_list

def todo_list_menu(app, todo_list):
  while True:
    utils.clear_screen()
    console.print(f"[green underline]{todo_list.title}:[/green underline]")
    if app.show_checked:
      shown_items = utils.todos_to_list(todo_list.todos)
    else:
      shown_items = utils.todos_to_list([todo for todo in todo_list.todos if not todo.checked])
    add_item_option = "[cyan]Add item[/cyan]"
    show_hide_option = f"{'Hide' if app.show_checked else 'Show'} checked items"
    change_list_option = "[bright_magenta]Switch list[/bright_magenta]"
    quit_option = "[red]Quit[/red]"
    options = shown_items + [add_item_option, show_hide_option, change_list_option, quit_option]
    selected = select(options)
    # Keep todo items visible after selecting an option
    for todo in shown_items:
      console.print(todo)
    if selected == add_item_option:
      todo_list.add_item(todo_list.todos)
      file_name = utils.todo_list_name_to_file_name(todo_list.title)
      utils.save_to_file(todo_list.todos, file_name)
    elif selected == show_hide_option:
      app.show_checked = not app.show_checked
    elif selected == change_list_option:
      return
    elif selected == quit_option:
      if confirm("Are you sure you want to quit?", default_is_yes=True):
        sys.exit()
    else:
      todo_options_menu(selected, todo_list)

def main():
  # TODO handle case when there are no json files
  app = TodoApp(utils.get_todo_lists())
  while True:
    utils.clear_screen()
    todo_list = choose_todo_list(app)
    selected = todo_list_menu(app, todo_list)
    
main()