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
      modified_todo_text = prompt("Edit todo:", initial_value=self.text).strip()
    self.text = modified_todo_text