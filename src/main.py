from generate import copy_static_to_public, generate_page


def main():
    copy_static_to_public()
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html",
    )


if __name__ == "__main__":
    main()
