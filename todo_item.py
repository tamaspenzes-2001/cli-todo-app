from beaupy import prompt

class TodoItem:
  def __init__(self, text, checked):
    self.text = text
    self.checked = checked

  def toggle_checked(self):
    self.checked = not self.checked

  def edit_text(self):
    modified_todo_text = ""
    while modified_todo_text == "":
      try:
        modified_todo_text = prompt("Edit todo (cannot contain \\):", initial_value=self.text).strip()
      except: # prevent program from crashing if "\" is typed
        continue
    self.text = modified_todo_text