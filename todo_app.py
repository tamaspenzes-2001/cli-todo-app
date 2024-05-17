from beaupy import prompt, confirm
from rich.console import Console
import utils

console = Console()

class TodoApp:
  def __init__(self, todo_lists):
    self.todo_lists = todo_lists
    self.loaded_todo_lists = []
    self.show_checked = False

  def create_list(self):
    utils.print_todos(self.todo_lists)
    print("")
    new_list = ""
    while not utils.is_list_name_valid(new_list):
      try:
        new_list = prompt("Name of new list (cannot contain any of these: . / \\):").strip()
        if new_list in self.todo_lists:
          console.print("[red]There's already a list with this name.[/red]")
          new_list = ""
      except: # prevent program from crashing if "\" is typed
        continue
    self.todo_lists.append(new_list)
    self.todo_lists.sort()
    utils.save_to_file([], new_list)

  def toggle_checked_items(self):
    self.show_checked = not self.show_checked

  def rename_list(self, todo_list):
    modified_title = ""
    while not utils.is_list_name_valid(modified_title):
      try:
        modified_title = prompt("Edit list title (cannot contain any of these: . / \\):", initial_value=todo_list.get_title()).strip()
        if modified_title != todo_list.get_title() and modified_title in self.todo_lists:
          console.print("[red]There's already a list with this name.[/red]")
          modified_title = ""
      except: # prevent program from crashing if "\" is typed
        continue
    list_index = self.todo_lists.index(todo_list.get_title())
    file_name = todo_list.get_title()
    todo_list.set_title(modified_title)
    self.todo_lists[list_index] = todo_list.get_title()
    self.todo_lists.sort()
    new_file_name = todo_list.get_title()
    utils.rename_file(file_name, new_file_name)

  def delete_list(self, todo_list):
    if confirm(f'Are you sure? All todos in this list will be lost. Forever!', default_is_yes=True):
      self.todo_lists.remove(todo_list.title)
      self.loaded_todo_lists.remove(todo_list)
      utils.delete_file(todo_list.get_title())
      del todo_list
      utils.restart_program()