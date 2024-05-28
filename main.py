from beaupy import confirm, select
from rich.console import Console
import sys
import utils
from todo_app import TodoApp
from todo_list import TodoList
from todo_item import TodoItem

console = Console()

def todo_options_menu(todo_hierarchy, printable_item, app):
  console.print("[cyan2]Selected: " + printable_item + "[/cyan2]")
  options = ["1. Toggle check", "2. Edit todo text", "3. Delete", "4. Move up", "5. Move down", "6. Edit subitems"]
  operation = select(options, return_index=True)
  todo_hierarchy[-1] = utils.find_todo_item(todo_hierarchy[-1].text, todo_hierarchy[-2].items)
  match operation:
    case 0: todo_hierarchy[-1].toggle_checked()
    case 1: todo_hierarchy[-1].edit_text()
    case 2: todo_hierarchy[-2].remove_item(todo_hierarchy[-1])
    case 3: todo_hierarchy[-2].move_item_up(todo_hierarchy[-1])
    case 4: todo_hierarchy[-2].move_item_down(todo_hierarchy[-1])
    case 5: todo_list_menu(app, todo_hierarchy)
  app.storage.save_to_file(todo_hierarchy[0], False)

def todo_list_menu(app, todo_hierarchy):
  while True:
    utils.clear_screen()
    header_text = "[chartreuse1 underline]"
    for item in todo_hierarchy:
      header_text += item.text + " / "
    header_text += "[/chartreuse1 underline]"
    console.print(header_text)
    shown_items = get_todos_to_show(app, todo_hierarchy[-1])
    add_subitem_option = "[cyan2]Add subitem[/cyan2]"
    settings_option = f"{'List' if type(todo_hierarchy[-1]) is TodoList else 'Todo'} settings"
    go_back_option = "[plum1]Go back[/plum1]"
    quit_option = "[salmon1]Quit[/salmon1]"
    options = shown_items + [add_subitem_option, settings_option, go_back_option, quit_option]
    selected = select(options)
    utils.print_todos(shown_items)
    if selected == add_subitem_option:
      todo_hierarchy[-1].add_item()
      app.storage.save_to_file(todo_hierarchy[0], False)
    elif selected == "Todo settings":
      todo_settings_menu(app, todo_hierarchy)
    elif selected == "List settings":
      list_settings_menu(app, todo_hierarchy[-1])
    elif selected == go_back_option:
      return
    elif selected == quit_option:
      if confirm("Are you sure you want to quit?", default_is_yes=True):
        sys.exit()
    else:
      printable_item = selected.split("\n")[0]
      todo_item = utils.find_todo_item(utils.strip_todo_decoration(printable_item), todo_hierarchy[-1].items)
      todo_options_menu(todo_hierarchy + [todo_item], printable_item, app)

def choose_todo_list(app):
  while True:
    utils.clear_screen()
    console.print("[chartreuse1 underline]TODO LISTS[/chartreuse1 underline]")
    create_list_option = "[cyan2]Create new list[/cyan2]"
    quit_option = "[salmon1]Quit[/salmon1]"
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

def todo_settings_menu(app, todo_hierarchy):
  console.print(f"[cyan2]Todo settings:[/cyan2]")
  show_hide_option = f"{'Hide' if app.show_checked else 'Show'} checked subitems"
  rename_option = "Edit todo text"
  delete_option = "[salmon1]Delete todo[/salmon1]"
  options = [show_hide_option, rename_option, delete_option]
  selected = select(options, return_index=True)
  match selected:
    case 0: app.toggle_checked_items()
    case 1:
      todo_hierarchy[-1].edit_text()
      app.storage.save_to_file(todo_hierarchy[0], False)
    case 2:
      todo_hierarchy[-2].remove_item(todo_hierarchy[-1])
      app.storage.save_to_file(todo_hierarchy[0], False)
      utils.restart_program()

def list_settings_menu(app, todo_list):
  console.print(f"[cyan2]List settings:[/cyan2]")
  show_hide_option = f"{'Hide' if app.show_checked else 'Show'} checked items"
  rename_option = "Rename list"
  delete_option = "[salmon1]Delete list[/salmon1]"
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

def main():
  app = TodoApp()
  while True:
    utils.clear_screen()
    if len(app.storage.todo_lists) == 0:
      console.print("[salmon1]There aren't any todo lists available.[/salmon1]")
      app.create_list()
    todo_list = choose_todo_list(app)
    selected = todo_list_menu(app, [todo_list])

main()