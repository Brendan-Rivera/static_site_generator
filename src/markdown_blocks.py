from enum import Enum
import re
from helper import text_to_textnodes
from textnode import TextNode, TextType
from htmlnode import HTMLNode 
from parentnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

# Markdown Block Section
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_list = []
    for block in blocks:
        block = block.strip()
        if block:
            blocks_list.append(block)
    return blocks_list

def block_to_block_type(block):
    lines = block.split("\n")

    # Heading: starts with one or more #
    if block.startswith("#"):
        return BlockType.HEADING

    # Code block: starts and ends with triple backticks (```), not '''
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # Quote block: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with -
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with number followed by dot (1. 2. etc.)
    if all(line.lstrip().startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    # Default: paragraph
    return BlockType.PARAGRAPH


#Functions to convert markdown to html_nodes
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node.text_node_to_html_node()
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    block = block.strip()
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    block = block.strip()
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level == 0 or level > 6:
        raise ValueError(f"Invalid heading level in block: {block}")
    text = block[level:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    match = re.match(r"```(?:\w+)?\n(.*?)\n```", block.strip(), re.DOTALL)
    if not match:
        raise ValueError(f"Invalid code block: {block}")
    text = match.group(1)
    raw_text_node = TextNode(text, TextType.TEXT)
    child = raw_text_node.text_node_to_html_node()
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def ordered_list_to_html_node(block):
    items = block.strip().split("\n")
    html_items = []
    for item in items:
        if not re.match(r"\d+\.", item.strip()):
            raise ValueError(f"Invalid ordered list item: {item}")
        text = item.lstrip("0123456789. ").strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html_node(block):
    items = block.strip().split("\n")
    html_items = []
    for item in items:
        if not item.strip().startswith(("-", "*")):
            raise ValueError(f"Invalid unordered list item: {item}")
        text = item.lstrip("-* ").strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.strip().split("\n")
    new_lines = []
    for line in lines:
        if not line.strip().startswith(">"):
            raise ValueError(f"Invalid quote line: {line}")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.QUOTE:  
            return quote_to_html_node(block)
        case _:
            raise ValueError(f"Invalid block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        child_nodes.append(html_node)
    return ParentNode("div", child_nodes, None)
            