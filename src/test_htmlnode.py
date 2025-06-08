import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode("a", "This is a test", [], {"href": "https://www.google.com",
        "target": "_blank",})
        test_output =  'href="https://www.google.com" target="_blank"'
        test_node = node.props_to_html()
        self.assertEqual(test_output, test_node)
    
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        node = HTMLNode("a", "This is a test", [], {"href": "https://www.google.com",
        "target": "_blank",})
        test_target = f"HTMLNode\nTag: {node.tag}\nValue: {node.value}\nChildren: {node.children}\nProps: {node.props}"
        self.assertEqual(test_target, node.__repr__())