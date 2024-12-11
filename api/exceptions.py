class ApiResultException(Exception):

  def __init__(self, msg, context={}):
    super().__init__(msg)
    self.context = context
