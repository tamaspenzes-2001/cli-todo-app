from beaupy import prompt
from todo_list import TodoList

class TodoItem(TodoList):
  def __init__(self, text, checked, todos):
    TodoList.__init__(self, text, todos)
    self.checked = checked

  def toggle_checked(self):
    self.checked = not self.checked
    for item in self.items:
      item.checked = self.checked
      for subitem in item.items:
        subitem.checked = self.checked

  def edit_text(self):
    modified_todo_text = ""
    while modified_todo_text == "":
      try:
        modified_todo_text = prompt("Edit todo (cannot contain \\):", initial_value=self.text).strip()
      except: # prevent program from crashing if "\" is typed
        continue
    self.text = modified_todo_text