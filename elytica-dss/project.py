class Project:
  def __init__(self, data):
    if "id" not in data:
      raise KeyError("data does not contain an id field.")
    if "name" not in data:
      raise KeyError("data does not contain a name field.")
    if "description" not in data:
      raise KeyError("data does not contain a description field.")
    if "application_id" not in data:
      raise KeyError("data does not contain an application_id field.")
    self.id = data['id']
    self.name = data['name']
    self.application_id = data['application_id']
    self.description = data['description']
    
  
