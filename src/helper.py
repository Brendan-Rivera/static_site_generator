import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes= []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        new_list = node.text.split(f"{delimiter}")

      #  if len(new_list) % 2 == 0:
       #     raise ValueError("Delimiter error found. Enclose texts in delimiters")

        for num, item in enumerate(new_list):
            if num % 2 == 0:
                new_nodes.append(TextNode(item.strip(), TextType.TEXT, node.url))
            else:
                new_nodes.append(TextNode(item.strip(), text_type, node.url))
        
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)



def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        find_pattern = extract_markdown_images(node.text)

        if len(find_pattern) == 0:
            new_nodes.append(node)
            continue

        node_text = node.text

        for alt, url in find_pattern:
            segment = node_text.split(f'![{alt}]({url})', 1)

            if len(segment) != 2:
                raise ValueError("Markdown for image was not closed")

            if segment[0] != "":
                new_nodes.append(TextNode(segment[0], TextType.TEXT))

            new_nodes.append(TextNode(f"{alt}", TextType.IMAGE, f"{url}"))

            node_text = segment[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text.strip(), TextType.TEXT))
    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        find_pattern = extract_markdown_links(node.text)

        if len(find_pattern) == 0:
            new_nodes.append(node)
            continue

        node_text = node.text

        for alt, url in find_pattern:

            segment = node_text.split(f'[{alt}]({url})', 1)

            if len(segment) != 2:
                raise ValueError("Markdown for link was not closed")

            if segment[0] != "":
                new_nodes.append(TextNode(segment[0], TextType.TEXT))

            new_nodes.append(TextNode(f"{alt}", TextType.LINK, f"{url}"))

            node_text = segment[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text.strip(), TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes



