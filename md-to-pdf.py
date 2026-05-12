#!/usr/bin/env python3
"""
Convert README.md to PDF.
This script tries pandoc first, then installs/uses Python packages if needed.
"""

import importlib
import subprocess
import sys
from pathlib import Path


def import_or_install(module_name, package_name=None):
    package_name = package_name or module_name
    try:
        return importlib.import_module(module_name)
    except ImportError:
        print(f"Package '{module_name}' is missing. Installing {package_name}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--user", package_name], check=True)
            return importlib.import_module(module_name)
        except subprocess.CalledProcessError:
            return None


def convert_with_pandoc(input_file, output_file):
    try:
        subprocess.run([
            "pandoc",
            input_file,
            "-o",
            output_file,
            "--from",
            "markdown",
            "--to",
            "pdf",
            "--standalone",
            "--pdf-engine=xelatex",
        ], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_with_weasyprint(input_file, output_file):
    markdown = import_or_install("markdown")
    weasyprint = import_or_install("weasyprint")
    if markdown is None or weasyprint is None:
        return False

    from weasyprint import HTML

    with open(input_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=["tables", "extra"])
    full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 2cm; line-height: 1.6; color: #333; }}
        h1, h2, h3, h4 {{ color: #2c3e50; margin-top: 1em; }}
        h1 {{ font-size: 2em; border-bottom: 3px solid #2c3e50; padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.5em; border-bottom: 2px solid #34495e; padding-bottom: 0.2em; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1.5em 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        th, td {{ border: 1px solid #bdc3c7; padding: 12px; text-align: left; }}
        th {{ background-color: #34495e; color: white; font-weight: bold; }}
        tr:nth-child(even) {{ background-color: #ecf0f1; }}
        code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        ul, ol {{ margin: 1em 0; padding-left: 2em; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

    try:
        HTML(string=full_html).write_pdf(output_file)
        return True
    except Exception as exc:
        print(f"Error generating PDF with WeasyPrint: {exc}", file=sys.stderr)
        return False


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "README.pdf"

    if not Path(input_file).exists():
        print(f"Error: {input_file} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Converting {input_file} to {output_file}...")

    if convert_with_pandoc(input_file, output_file):
        print(f"✓ PDF generated using pandoc: {output_file}")
        sys.exit(0)

    if convert_with_weasyprint(input_file, output_file):
        print(f"✓ PDF generated using weasyprint: {output_file}")
        sys.exit(0)

    print("Error: No PDF conversion tool available.", file=sys.stderr)
    print("\nPlease install one of the following:", file=sys.stderr)
    print("  Pandoc (recommended):", file=sys.stderr)
    print("    Ubuntu/Debian: apt-get update && apt-get install pandoc texlive-latex-base texlive-latex-extra", file=sys.stderr)
    print("\n  WeasyPrint (Python):", file=sys.stderr)
    print("    python3 -m pip install --user weasyprint markdown", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
