class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        else:
            return "".join(f' {key}="{value}"' for key, value in self.props.items())
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("A LeafNode must have a value.")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return NotImplemented # Or False, depending on desired strictness
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and # Ensure this attribute is compared
                self.props == other.props)
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode object must have tag.")
        if self.children is None:
            raise ValueError("ParentNode object must have children nodes.")
        
        else:
            html_strings = []
            for child in self.children:
                html_strings.append(child.to_html())

            children_html = "".join(html_strings)

            return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        
        
        


        

        




