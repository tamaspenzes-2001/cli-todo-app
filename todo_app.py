from beaupy import prompt, confirm
from rich.console import Console
from todo_list import TodoList
from todo_storage_manager import TodoStorageManager
import utils

console = Console()

class TodoApp:
  def __init__(self):
    self.storage = TodoStorageManager()
    self.storage.get_todo_lists()
    self.show_checked = False

  def create_list(self):
    utils.print_todos(self.storage.todo_lists)
    print("")
    list_name = ""
    while not utils.is_list_name_valid(list_name):
      try:
        list_name = prompt("Name of new list (cannot contain any of these: . / \\):").strip()
        if list_name in self.storage.todo_lists:
          console.print("[salmon1]There's already a list with this name.[/salmon1]")
          list_name = ""
      except: # prevent program from crashing if "\" is typed
        continue
    self.storage.save_to_file(TodoList(list_name, []), True)

  def toggle_checked_items(self):
    self.show_checked = not self.show_checked

  def rename_list(self, todo_list):
    modified_title = ""
    while not utils.is_list_name_valid(modified_title):
      try:
        modified_title = prompt("Edit list title (cannot contain any of these: . / \\):", initial_value=todo_list.get_title()).strip()
        if modified_title != todo_list.get_title() and modified_title in self.todo_lists:
          console.print("[salmon1]There's already a list with this name.[/salmon1]")
          modified_title = ""
      except: # prevent program from crashing if "\" is typed
        continue
    list_index = self.storage.todo_lists.index(todo_list.get_title())
    file_name = todo_list.get_title()
    todo_list.set_title(modified_title)
    self.storage.todo_lists[list_index] = todo_list.get_title()
    self.storage.todo_lists.sort()
    new_file_name = todo_list.get_title()
    self.storage.rename_file(file_name, new_file_name)
    self.storage.save_to_file(todo_list, False)

  def delete_list(self, todo_list):
    if confirm(f'Are you sure? All todos in this list will be lost. Forever!', default_is_yes=True):
      self.storage.todo_lists.remove(todo_list.text)
      self.storage.loaded_todo_lists.remove(todo_list)
      self.storage.delete_file(todo_list.get_title())
      del todo_list
      utils.restart_program()