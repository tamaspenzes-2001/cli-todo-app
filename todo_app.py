from beaupy import prompt
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
