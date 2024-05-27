from beaupy import prompt
from todo_list import TodoList

class TodoItem(TodoList):
  def __init__(self, title, checked, todos):
    TodoList.__init__(self, title, todos)
    self.checked = checked

  def toggle_checked(self):
    self.checked = not self.checked

  def edit_text(self):
    modified_todo_text = ""
    while modified_todo_text == "":
      try:
        modified_todo_text = prompt("Edit todo (cannot contain \\):", initial_value=self.title).strip()
      except: # prevent program from crashing if "\" is typed
        continue
    self.title = modified_todo_text