
class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        e_str = ""
        if self.props is None:
            return ""

        for k, v in self.props.items():
            e_str += f'{k}="{v}" '
        
        return e_str.rstrip(" ")

    def __repr__(self):
        return f"HTMLNode\nTag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"