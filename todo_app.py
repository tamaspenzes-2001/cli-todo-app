class TodoApp:
  def __init__(self, todo_lists):
    self.todo_lists = todo_lists
    self.loaded_todo_lists = []
    self.show_checked = False