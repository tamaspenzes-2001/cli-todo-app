with open("todos.txt") as todos_doc:
  for todo in todos_doc:
    print(todo.strip())