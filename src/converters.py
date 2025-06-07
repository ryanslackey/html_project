from htmlnode import LeafNode
from textnode import TextNode
from textnode import TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=f"{text_node.text}")
        case TextType.BOLD:
            return LeafNode(tag="b", value=f"{text_node.text}")
        case TextType.ITALIC:
            return LeafNode(tag="i", value=f"{text_node.text}")
        case TextType.CODE:
            return LeafNode(tag="code", value=f"{text_node.text}")
        case TextType.LINK:
            return LeafNode(tag="a", value=f"{text_node.text}", props={"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": f"{text_node.url}", "alt": f"{text_node.text}"})
        
        case _:
            raise Exception("TextNode does not have a valid TextType")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == "TEXT":
            if delimiter in node.text:
                split_text = node.text.split(delimiter)
                if len(split_text) % 2 == 1:
                    raise Exception("Invalid Markdown syntax.")
                else:
                    for i,text in enumerate(split_text):
                        if i % 2 == 0:
                            new_nodes.append(TextNode(text, "text"))
                        else:
                            new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(node)
        else: 
            new_nodes.append(node)        
    
    return new_nodes
                     

        
 
            

