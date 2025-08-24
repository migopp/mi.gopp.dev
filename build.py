import os
from pathlib import Path
import subprocess
import shutil
from typing import Literal

def from_template(temp: Literal["base"]):
    template_file_str = f"{temp}.html"
    template_path_str = str(Path("template") / template_file_str)
    with open(template_path_str, 'r', encoding='utf-8') as f:
        return f.read()

def file_to_html(md_path, html_path):
    if (not html_path.exists()):
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.touch

    try:
        md_result = subprocess.run(["kramdown", str(md_path)], capture_output=True, text=True, check=True)
        md = md_result.stdout;
    except subprocess.CalledProcessError as e:
        print(f"[BUILD] Failed to convert {md_path}: {e}")

    template_contents = from_template("base")
    html = template_contents.replace("{{CONTENT}}", md)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

def glob_to_html(md_path_base_str, html_path_base_str):
    md_path_base = Path(md_path_base_str)
    html_path_base = Path(html_path_base_str)

    md_glob = list(md_path_base.glob("**/*.md"))
    for md_file in md_glob:
        path_incl_md_base_str, md_file_name_str = os.path.split(md_file)
        path_from_md_base = Path(path_incl_md_base_str).relative_to(md_path_base)
        path_from_html_base = html_path_base / path_from_md_base / md_file_name_str
        path_from_html_base = path_from_html_base.with_suffix(".html")
        file_to_html(md_file, path_from_html_base)

def copy_static_to(dest_str):
    dest_str = str(Path(dest_str) / "static")
    try:
        shutil.copytree("static", dest_str, dirs_exist_ok=True)
    except Exception as e:
        print(f"[BUILD] Failed to copy `static` to {dest}: {e}")

if __name__ == "__main__":
    src, dest = "root", "build"
    glob_to_html(src, dest)
    copy_static_to(dest)
