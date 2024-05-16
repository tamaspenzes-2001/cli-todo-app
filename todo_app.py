from beaupy import prompt, confirm
import utils

class TodoApp:
  def __init__(self, todo_lists):
    self.todo_lists = todo_lists
    self.loaded_todo_lists = []
    self.show_checked = False

  def create_list(self):
    new_list = ""
    while new_list == "":
      new_list = prompt("New list:").strip()
    self.todo_lists.append(new_list)
    file_name = utils.todo_list_name_to_file_name(new_list)
    utils.save_to_file([], file_name)

  def toggle_checked_items(self):
    self.show_checked = not self.show_checked

  def rename_list(self, todo_list):
    modified_title = ""
    while modified_title == "":
      modified_title = prompt("Edit list title:", initial_value=todo_list.get_title()).strip()
    list_index = self.todo_lists.index(todo_list.get_title())
    file_name = utils.todo_list_name_to_file_name(todo_list.get_title())
    todo_list.set_title(modified_title)
    self.todo_lists[list_index] = todo_list.get_title()
    new_file_name = utils.todo_list_name_to_file_name(todo_list.get_title())
    utils.rename_file(file_name, new_file_name)

  def delete_list(self, todo_list):
    if confirm(f'Are you sure? All todos in this list will be lost. Forever!', default_is_yes=True):
      self.todo_lists.remove(todo_list.title)
      self.loaded_todo_lists.remove(todo_list)
      file_name = utils.todo_list_name_to_file_name(todo_list.get_title())
      utils.delete_file(file_name)
      del todo_list
      utils.restart_program()