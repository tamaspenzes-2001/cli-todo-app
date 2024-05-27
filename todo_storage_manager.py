import json
import os
import jsonpickle
from todo_list import TodoList
from todo_item import TodoItem

class TodoStorageManager:
  def __init__(self):
    self.todo_lists = []
    self.loaded_todo_lists = []

  def read_todos_from_file(self, list_name):
    with open(f"todos/{list_name}.json") as todos_doc:
      todos_data = json.load(todos_doc)
      todo_list = jsonpickle.decode(todos_data)
      return todo_list

  def find_todo_list(self, list_name):
    todo_list = next((todo_list for todo_list in self.loaded_todo_lists if todo_list.text == list_name), None)
    if todo_list is None:
      todo_list = self.read_todos_from_file(list_name)
      self.loaded_todo_lists.append(todo_list)
    return todo_list

  def rename_file(self, list_name, new_list_name):
    os.rename(f"todos/{list_name}.json", f"todos/{new_list_name}.json")
    self.get_todo_lists()

  def delete_file(self, list_name):
    os.remove(f"todos/{list_name}.json")
    self.get_todo_lists()

  def process_todos_data(self, data, file):
    todo_list = []
    for todo_item in data:
      subitems = []
      for subitem in todo_item["items"]:
        subitems.append(TodoItem(subitem["text"], subitem["checked"], []))
      todo_list.append(TodoItem(todo_item["text"], todo_item["checked"], subitems))
    return TodoList(file.split(".")[0], todo_list)

  def save_to_file(self, list_to_save, new_list):
    with open(f"todos/{list_to_save.text}.json", "w") as todos_doc:
      json_string = jsonpickle.encode(list_to_save)
      json.dump(json_string, todos_doc)
      self.get_todo_lists()

  def get_todo_lists(self):
    if not os.path.isdir("todos"):
      os.makedirs("todos")
    todo_files = os.listdir("todos")
    todo_lists = []
    for file in todo_files:
      todo_lists.append(file.split(".")[0])
    todo_lists.sort()
    self.todo_lists = todo_lists