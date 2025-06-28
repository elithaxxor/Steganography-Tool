"""Simple Flask web interface to control Steganography Tool."""
from __future__ import annotations

import asyncio
from pathlib import Path

from flask import Flask, render_template_string, request

from stego_plugins import discover_plugins, PluginError

app = Flask(__name__)

FORM = """
<h1>Stego Web Control</h1>
<form method='post' enctype='multipart/form-data'>
Tool: <input name='tool'><br>
Action: <input name='action'><br>
Input file: <input type='text' name='infile'><br>
Payload: <input type='text' name='payload'><br>
Output: <input type='text' name='output'><br>
<input type='submit'>
</form>
<pre>{{ result }}</pre>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        tool = request.form.get("tool")
        action = request.form.get("action")
        infile = Path(request.form.get("infile"))
        payload = request.form.get("payload")
        output = Path(request.form.get("output", "out.bin"))

        plugin_cls = discover_plugins().get(tool)
        if not plugin_cls:
            result = f"Unknown tool: {tool}"
        else:
            try:
                plugin = plugin_cls()
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                if action == "embed":
                    loop.run_until_complete(plugin.embed(infile, Path(payload), output))
                elif action == "extract":
                    loop.run_until_complete(plugin.extract(infile, output))
                elif action == "detect" and hasattr(plugin, "detect"):
                    res = loop.run_until_complete(plugin.detect(infile))
                    result = str(res)
                else:
                    result = "Unsupported action"
                loop.close()
            except PluginError as exc:
                result = f"Error: {exc}"
    return render_template_string(FORM, result=result)


if __name__ == "__main__":
    app.run(port=8000)
