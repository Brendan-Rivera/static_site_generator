from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self, children=None):
        if  self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag is not None and self.props is not None:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        elif self.tag is not None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"{self.value}"
