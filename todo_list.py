from todo_item import TodoItem
from beaupy import prompt, confirm

class TodoList:
  def __init__(self, title, todos):
    self.title = title
    self.todos = todos
  
  def get_title(self):
    return self.title
    
  def set_title(self, new_title):
    self.title = new_title

  def add_item(self, todos):
    new_item = ""
    while new_item == "":
      try:
        new_item = prompt("New item (cannot contain \\):").strip()
      except: # prevent program from crashing if "\" is typed
        continue
    todos.append(TodoItem(new_item, False))

  def remove_item(self, selected_todo):
    if confirm(f'Delete item from the list?', default_is_yes=True):
      self.todos.remove(selected_todo)

  def move_item_up(self, selected_todo):
    todo_index = self.todos.index(selected_todo)
    if todo_index != 0:
      self.todos.insert(todo_index-1, self.todos.pop(todo_index))
    else:
      self.todos.append(self.todos.pop(todo_index))

  def move_item_down(self, selected_todo):
    todo_index = self.todos.index(selected_todo)
    if todo_index != len(self.todos)-1:
      self.todos.insert(todo_index+1, self.todos.pop(todo_index))
    else:
      self.todos.insert(0, self.todos.pop())