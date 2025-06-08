import unittest
import helper
from textnode import TextNode, TextType

class TestHelper(unittest.TestCase):

    def test_text_node_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = helper.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a", TextType.TEXT),
                                        TextNode("code block", TextType.CODE),
                                        TextNode("word", TextType.TEXT),
                                    ])

    def test_text_node_code_multiple(self):
        node = [TextNode("This is text with a `code block` word", TextType.TEXT) , TextNode("Node test case number 2 has `another text node` here", TextType.TEXT)]
        new_nodes = helper.split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a", TextType.TEXT),
                                        TextNode("code block", TextType.CODE),
                                        TextNode("word", TextType.TEXT),
                                        TextNode("Node test case number 2 has", TextType.TEXT),
                                        TextNode("another text node", TextType.CODE),
                                        TextNode("here", TextType.TEXT),
                                    ])

    def test_text_node_bold(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = helper.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a", TextType.TEXT),
                                        TextNode("code block", TextType.BOLD),
                                        TextNode("word", TextType.TEXT),
                                    ])
    
    def test_extract_markdown_images(self):
        matches = helper.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_images_multiple(self):
        matches = helper.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![notanImage](https://i.imgur.com/jzkycJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("notanImage" , "https://i.imgur.com/jzkycJKZ.png")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = helper.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link_one](https://i.imgur.com/zjjcJKZ.png) and another [link_two](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = helper.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link_one", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link_two", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        new_nodes = helper.text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is", TextType.TEXT, None), 
                TextNode("text", TextType.BOLD, None), 
                TextNode( "with an", TextType.TEXT, None), 
                TextNode("italic", TextType.ITALIC, None), 
                TextNode( "word and a", TextType.TEXT, None), 
                TextNode("code block", TextType.CODE, None), 
                TextNode( "and an ", TextType.TEXT, None), 
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode( "and a", TextType.TEXT, None), 
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
                new_nodes
        )
    
