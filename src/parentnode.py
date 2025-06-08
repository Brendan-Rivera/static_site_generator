from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag,children=children,props=props)

    def to_html(self, children=None):
        if not self.tag:
            raise ValueError("Parent Node doesn't have a tag")
        
        props_str = ""
        if self.props:
            props_str = ' ' + ' '.join(f'{k}="{v}"' for k, v in self.props.items())

        inner_html = ""
        if self.children:
            inner_html = ' '.join(child.to_html() for child in self.children)
        else:
            raise ValueError("Parent Node has no children")

        return f"<{self.tag}{props_str}>{inner_html}</{self.tag}>"