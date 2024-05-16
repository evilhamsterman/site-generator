import os
import shutil


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
