class Job:
  def __init__(self, data):
    if "id" not in data:
      raise KeyError("data does not contain an id field.")
    if "name" not in data:
      raise KeyError("data does not contain a name field.")
    if "status" not in data:
      raise KeyError("data does not contain a status field.")
    if "output" not in data:
      raise KeyError("data does not contain an output field.")
    self.id = data['id']
    self.status = data['status']
    self.output = data['output']
    self.name = data['name']
    
  
