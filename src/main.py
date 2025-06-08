import os
import shutil
from markdown_blocks import markdown_to_html_node
from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode

def clean_copy_dir():
    public_dir = "public"
    static_dir = "static"

    # Remove public directory if it exists
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    # Recreate the public directory
    os.makedirs(public_dir, exist_ok=True)

    # Walk through the static directory
    for root, dirs, files in os.walk(static_dir):
        # Compute relative path from static_dir
        rel_path = os.path.relpath(root, static_dir)
        dest_root = os.path.join(public_dir, rel_path) if rel_path != "." else public_dir

        # Create directories in destination
        os.makedirs(dest_root, exist_ok=True)

        # Copy files
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)
            shutil.copy2(src_file, dest_file)

def extract_title(markdown):
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    raise ValueError("No H1 header found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    
    with open(template_path, "r", encoding="utf-8") as template:
        template_content = template.read()

    html_string = markdown_to_html_node(markdown_content)
    html_string = html_string.to_html()

    title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)


    with open(dest_path, "w", encoding="utf-8") as dest:
        dest.write(template_content)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if not file.endswith(".md"):
                continue  # skip non-markdown files

            # Full path to the markdown file
            full_path = os.path.join(root, file)

            # Relative path to preserve directory structure
            relative_dir = os.path.relpath(root, dir_path_content)
            relative_output_dir = os.path.join(dest_dir_path, relative_dir)

            # Ensure output directory exists
            os.makedirs(relative_output_dir, exist_ok=True)

            # Destination file path with .html extension
            output_filename = os.path.splitext(file)[0] + ".html"
            dest_path = os.path.join(relative_output_dir, output_filename)

            # Generate the page
            generate_page(full_path, template_path, dest_path)
def main():
    clean_copy_dir()
    generate_pages_recursive("content/", "template.html", "./public")

main()