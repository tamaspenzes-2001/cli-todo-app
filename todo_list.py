from beaupy import prompt, confirm

class TodoList:
  def __init__(self, text, items):
    self.text = text
    self.items = items
  
  def get_title(self):
    return self.text
    
  def set_title(self, new_title):
    self.text = new_title

  def add_item(self):
    from todo_item import TodoItem
    new_item = ""
    while new_item == "":
      try:
        item_or_subitem = "item" if type(self) is TodoList else "subitem"
        new_item = prompt(f"New {item_or_subitem} (cannot contain \\):").strip()
      except: # prevent program from crashing if "\" is typed
        continue
    self.items.append(TodoItem(new_item, False, []))

  def remove_item(self, selected_todo):
    if confirm(f'Delete item from the list?', default_is_yes=True):
      self.items.remove(selected_todo)
      del selected_todo

  def move_item_up(self, selected_todo):
    todo_index = self.items.index(selected_todo)
    if todo_index != 0:
      self.items.insert(todo_index-1, self.items.pop(todo_index))
    else:
      self.items.append(self.items.pop(todo_index))

  def move_item_down(self, selected_todo):
    todo_index = self.items.index(selected_todo)
    if todo_index != len(self.items)-1:
      self.items.insert(todo_index+1, self.items.pop(todo_index))
    else:
      self.items.insert(0, self.items.pop())