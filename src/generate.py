import os
import shutil

from markdown_html import markdown_to_html_node


class TitleNotFoundError(Exception): ...


def copy_folder(source_path: str, dest_path: str):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    entries = os.listdir(source_path)
    for entry in entries:
        source = os.path.join(source_path, entry)
        dest = os.path.join(dest_path, entry)
        if os.path.isfile(source):
            shutil.copy(src=source, dst=dest)
        else:
            copy_folder(source_path=source, dest_path=dest)


def copy_static_to_public():
    public_path = "public"
    source_path = "static"
    # Clean public folder
    if os.path.exists(public_path):
        print("Cleaning public directory")
        shutil.rmtree(public_path)

    # Walk the tree
    print("Copying static files")
    copy_folder(source_path=source_path, dest_path=public_path)


def extract_title(markdown) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            title = line[2:]
            return title
    raise TitleNotFoundError("No title found in document")


def replace_placeholder(template: str, value: str, placeholder: str) -> str:
    template_parts = template.split(placeholder)
    return value.join(template_parts)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read file data
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()

    # Covert
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    # Replace placeholders
    template = replace_placeholder(template, title, "{{ Title }}")
    template = replace_placeholder(template, html, "{{ Content }}")

    # Write out files
    with open(dest_path, "w") as file:
        file.write(template)
