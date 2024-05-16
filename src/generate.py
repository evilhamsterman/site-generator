import os
import shutil
from pathlib import Path

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


def generate_page(
    from_path: str | Path, template_path: str | Path, dest_path: str | Path
) -> None:
    from_path = Path(from_path)
    template_path = Path(template_path)
    dest_path = Path(dest_path)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read file data
    markdown = from_path.read_text()
    template = template_path.read_text()

    # Covert
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    # Replace placeholders
    template = replace_placeholder(template, title, "{{ Title }}")
    template = replace_placeholder(template, html, "{{ Content }}")

    # Write out files
    dest_path.write_text(template)


def generate_pages_recursive(
    content_dir_path: str | Path, template_path: str | Path, dest_dir_path: str | Path
) -> None:
    content_dir_path = Path(content_dir_path)
    template_path = Path(template_path)
    dest_dir_path = Path(dest_dir_path)
    for _, directories, files in content_dir_path.walk():
        for file in files:
            dest = dest_dir_path / file.replace("md", "html")
            file = content_dir_path / file
            generate_page(from_path=file, template_path=template_path, dest_path=dest)
        for directory in directories:
            content = content_dir_path / directory
            dest = dest_dir_path / directory
            if not dest.is_dir() and not dest.exists():
                dest.mkdir()
            generate_pages_recursive(
                content_dir_path=content,
                template_path=template_path,
                dest_dir_path=dest,
            )
