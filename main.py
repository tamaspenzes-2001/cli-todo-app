from beaupy import confirm, select
from rich.console import Console
import sys
import utils
from todo_app import TodoApp
from todo_item import TodoItem

console = Console()

def todo_options_menu(selected_todo, todo_list, app):
  console.print(f"[cyan]Selected: {selected_todo}[/cyan]")
  options = ["1. Toggle check", "2. Edit todo text", "3. Delete", "4. Move up", "5. Move down", "6. Edit subitems"]
  operation = select(options, return_index=True)
  selected_todo = utils.find_todo_item(selected_todo, todo_list.items)
  match operation:
    case 0: selected_todo.toggle_checked()
    case 1: selected_todo.edit_text()
    case 2: todo_list.remove_item(selected_todo)
    case 3: todo_list.move_item_up(selected_todo)
    case 4: todo_list.move_item_down(selected_todo)
    case 5: todo_subitems_menu(selected_todo, todo_list, app)
  app.storage.save_to_file(todo_list, False)

def todo_subitem_options_menu(selected_todo, todo, app):
  console.print(f"[cyan]Selected: {selected_todo}[/cyan]")
  options = ["1. Toggle check", "2. Edit todo text", "3. Delete", "4. Move up", "5. Move down"]
  operation = select(options, return_index=True)
  selected_todo = utils.find_todo_item(selected_todo, todo.items)
  match operation:
    case 0: selected_todo.toggle_checked()
    case 1: selected_todo.edit_text()
    case 2: todo.remove_item(selected_todo)
    case 3: todo.move_item_up(selected_todo)
    case 4: todo.move_item_down(selected_todo)
  todo_list = next((loaded_todo_list for loaded_todo_list in app.storage.loaded_todo_lists if todo in loaded_todo_list.items))
  app.storage.save_to_file(todo_list, False)

def todo_subitems_menu(todo, todo_list, app):
  while True:
    utils.clear_screen()
    console.print(f"[green underline]{todo_list.title} / {todo.title}:[/green underline]")
    shown_items = get_todos_to_show(app, todo)
    add_subitem_option = "[cyan]Add subitem[/cyan]"
    todo_settings = "Todo settings"
    go_back_option = "[bright_magenta]Go back[/bright_magenta]"
    quit_option = "[red]Quit[/red]"
    options = shown_items + [add_subitem_option, todo_settings, go_back_option, quit_option]
    selected = select(options)
    utils.print_todos(shown_items)
    if selected == add_subitem_option:
      todo.add_item()
      app.storage.save_to_file(todo_list, False)
    elif selected == todo_settings:
      todo_settings_menu(app, todo, todo_list)
    elif selected == go_back_option:
      return
    elif selected == quit_option:
      if confirm("Are you sure you want to quit?", default_is_yes=True):
        sys.exit()
    else:
      todo_subitem_options_menu(selected, todo, app)

def choose_todo_list(app):
  while True:
    utils.clear_screen()
    console.print("[green underline]TODO LISTS[/green underline]")
    create_list_option = "[cyan]Create new list[/cyan]"
    quit_option = "[red]Quit[/red]"
    options = app.storage.todo_lists + [create_list_option, quit_option]
    user_selection = select(options)
    if user_selection == create_list_option:
      app.create_list()
    elif user_selection == quit_option:
      if confirm("Are you sure you want to quit?", default_is_yes=True):
        sys.exit()
    else:
      todo_list = app.storage.find_todo_list(user_selection)
      return todo_list

def todo_settings_menu(app, todo_item, todo_parent):
  console.print(f"[cyan]Todo settings:[/cyan]")
  show_hide_option = f"{'Hide' if app.show_checked else 'Show'} checked subitems"
  rename_option = "Edit todo text"
  delete_option = "[red]Delete todo[/red]"
  options = [show_hide_option, rename_option, delete_option]
  selected = select(options, return_index=True)
  match selected:
    case 0: app.toggle_checked_items()
    case 1:
      todo_item.edit_text()
      app.storage.save_to_file(todo_parent, False)
    case 2:
      todo_parent.remove_item(todo_item)
      app.storage.save_to_file(todo_parent, False)
      utils.restart_program()

def list_settings_menu(app, todo_list):
  console.print(f"[cyan]List settings:[/cyan]")
  show_hide_option = f"{'Hide' if app.show_checked else 'Show'} checked items"
  rename_option = "Rename list"
  delete_option = "[red]Delete list[/red]"
  options = [show_hide_option, rename_option, delete_option]
  selected = select(options, return_index=True)
  match selected:
    case 0: app.toggle_checked_items()
    case 1: app.rename_list(todo_list)
    case 2: app.delete_list(todo_list)

def get_todos_to_show(app, todo_list):
  if app.show_checked:
    return utils.todos_to_list(app, todo_list.items)
  else:
    return utils.todos_to_list(app, [todo for todo in todo_list.items if not todo.checked])

def todo_list_menu(app, todo_list):
  while True:
    utils.clear_screen()
    console.print(f"[green underline]{todo_list.title}:[/green underline]")
    shown_items = get_todos_to_show(app, todo_list)
    add_item_option = "[cyan]Add item[/cyan]"
    todo_settings = "List settings"
    go_back_option = "[bright_magenta]Switch list[/bright_magenta]"
    quit_option = "[red]Quit[/red]"
    options = shown_items + [add_item_option, todo_settings, go_back_option, quit_option]
    selected = select(options)
    utils.print_todos(shown_items)
    if selected == add_item_option:
      todo_list.add_item()
      app.storage.save_to_file(todo_list, False)
    elif selected == todo_settings:
      list_settings_menu(app, todo_list)
    elif selected == go_back_option:
      return
    elif selected == quit_option:
      if confirm("Are you sure you want to quit?", default_is_yes=True):
        sys.exit()
    else:
      todo_options_menu(selected.split("\n")[0], todo_list, app)

def main():
  app = TodoApp()
  while True:
    utils.clear_screen()
    if len(app.storage.todo_lists) == 0:
      console.print("[red]There aren't any todo lists available.[/red]")
      app.create_list()
    todo_list = choose_todo_list(app)
    selected = todo_list_menu(app, todo_list)

main()