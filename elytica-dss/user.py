class User:
  def __init__(self, data):
    if "id" not in data:
      raise KeyError("data does not contain an id field.")
    if "name" not in data:
      raise KeyError("data does not contain a name field.")
    if "email" not in data:
      raise KeyError("data does not contain an email field.")
    if "rate_limit" not in data:
      raise KeyError("data does not contain a rate_limit field.")
    self.id = data['id']
    self.name = data['name']
    self.email = data['email']
    self.rate_limit = data['rate_limit']
