class InputFile:
  def __init__(self, data):
    if "id" not in data:
      raise KeyError("data does not contain an id field.")
    if "filename" not in data:
      raise KeyError("data does not contain a name field.")
    self.id = data['id']
    self.name = data['filename']
    
  
