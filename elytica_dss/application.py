class Application:
  def __init__(self, data):
    if "id" not in data:
      raise KeyError("data does not contain an id field.")
    if "executable_name" not in data:
      raise KeyError("data does not contain an executable_name field.")
    if "executable_flags" not in data:
      raise KeyError("data does not contain a executable_flags field.")
    if "display_name" not in data:
      raise KeyError("data does not contain an application_id field.")
    self.id = data['id']
    self.display_name = data['display_name']
    self.executable_name = data['executable_name']
    self.executable_flags = data['executable_flags']

    
