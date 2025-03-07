from io import TextIOWrapper
import os
import shutil

from markdown_blocks import extract_title, markdown_to_html_node


def main() -> None:
    """
    Copy all files and directories from static directory into
    public directory. And generate all markdown files in
    content directory to html files in public directory.
    """
    root_dir: str = os.getcwd()
    source_dir: str = os.path.join(root_dir, "static/")
    dest_dir: str = os.path.join(root_dir, "public/")
    copy_static(source_dir, dest_dir)
    content_dir: str = os.path.join(root_dir, "content")
    template_path: str = os.path.join(root_dir, "template.html")
    generate_pages_recursive(content_dir, template_path, dest_dir)


def copy_static(src: str, dst: str) -> None:
    """
    Recursively copy all files and directories from src to dst.
    If dst exists, it will be deleted and recreated.

    Args:
        src: Source directory path
        dst: Destination directory path
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    entries: list[str] = os.listdir(src)
    for entry in entries:
        src_path: str = os.path.join(src, entry)
        dst_path: str = os.path.join(dst, entry)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path} to {dst_path}")
            continue
        print(f"Proccessing directory: {src_path}")
        copy_static(src_path, dst_path)


def generate_pages_recursive(
        content_dir: str, template_path: str, dest_path: str) -> None:
    entries: list[str] = os.listdir(content_dir)
    """
    Recursively generate pages from content directories into
    destination directories.

    Args:
        content_dir: Source directory path
        template_path: Source template path files
        dest_path: Destination directory path
    """
    for entry in entries:
        parent_dir: str = os.path.join(dest_path, entry)
        dest_dir: str = os.path.dirname(parent_dir)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        from_path: str = os.path.join(content_dir, entry)
        if os.path.isfile(from_path) and entry.endswith(".md"):
            html_file: str = entry.replace(".md", ".html")
            parent_dir = os.path.join(dest_dir, html_file)
            generate_page(from_path, template_path, parent_dir)
            continue
        generate_pages_recursive(from_path, template_path, parent_dir)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """
    Generating markdown file into html page using html template.
    Read both markdown and template, write it into new html.

    Args:
        from_path: Source markdown path files
        template_path: Source template path files
        dest_path: Destination new html path files
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_fd: TextIOWrapper = open(from_path, encoding="utf-8")
    template_fd: TextIOWrapper = open(template_path, encoding="utf-8")
    markdown: str = markdown_fd.read()
    template: str = template_fd.read()
    markdown_fd.close()
    template_fd.close()
    html: str = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", extract_title(markdown))
    template = template.replace("{{ Content }}", html)
    dest_dir: str = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)


if __name__ == "__main__":
    main()
