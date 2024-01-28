
DEFAULT_IMAGE_ATTRIBUTE = "title"

class Filter:
  def __init__(self, filter_string: str, image_attribute: str = DEFAULT_IMAGE_ATTRIBUTE):
    self.filter_string = filter_string
    self.image_attribute = image_attribute

