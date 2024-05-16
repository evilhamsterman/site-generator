from generate import copy_static_to_public, generate_pages_recursive


def main():
    copy_static_to_public()
    generate_pages_recursive(
        content_dir_path="content",
        template_path="template.html",
        dest_dir_path="public",
    )


if __name__ == "__main__":
    main()
