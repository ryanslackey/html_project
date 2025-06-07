from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url = None):
        if not isinstance(text_type, TextType):
            raise TypeError("The 'text_type' property must be an instance of the TextType enum")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            # Don't attempt to compare against unrelated types
            return NotImplemented
        return (self.text == other.text 
                and self.text_type == other.text_type 
                and self.url == other.url)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.text!r}, {self.text_type.value!r}, {self.url!r})"




        
