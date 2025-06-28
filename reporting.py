"""Generate HTML/JSON forensic reports from detection results."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Dict, Any

HTML_TEMPLATE = """<html><head><meta charset='utf-8'><title>Stego Report</title></head>
<body><h1>Detection Report</h1><table border='1'>
<tr><th>File</th><th>Tool</th><th>Result</th></tr>
{rows}
</table></body></html>"""


def json_to_html(results: Iterable[Dict[str, Any]]) -> str:
    rows = []
    for item in results:
        rows.append(
            f"<tr><td>{item.get('file')}</td><td>{item.get('tool')}</td><td>{item.get('result')}</td></tr>"
        )
    return HTML_TEMPLATE.format(rows="\n".join(rows))


def generate_report(json_path: Path, html_path: Path) -> None:
    data = json.loads(Path(json_path).read_text())
    html = json_to_html(data)
    Path(html_path).write_text(html)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate detection report")
    parser.add_argument("input", help="JSON input file")
    parser.add_argument("-o", "--output", default="report.html", help="HTML output file")
    args = parser.parse_args()
    generate_report(Path(args.input), Path(args.output))
    print(f"Report written to {args.output}")
