from __future__ import annotations

import asyncio
from pathlib import Path

from flask import Flask, jsonify, request, send_file

from stego_plugins import discover_plugins, PluginError

PLUGIN_MAP = discover_plugins()

app = Flask(__name__)


@app.post("/api/v3/plugin/<tool>/<action>")
def plugin_route(tool: str, action: str):
    args = request.json or {}
    infile = Path(args.get("infile", ""))
    payload = Path(args.get("payload", "")) if args.get("payload") else None
    output = Path(args.get("output", "output.bin"))

    plugin_cls = PLUGIN_MAP.get(tool)
    if not plugin_cls:
        return jsonify({"error": "unsupported tool"}), 400

    try:
        plugin = plugin_cls()
    except PluginError as exc:
        return jsonify({"error": str(exc)}), 500

    async def run():
        try:
            if action == "embed":
                await plugin.embed(infile, payload, output)
            elif action == "extract":
                await plugin.extract(infile, output)
            elif action == "detect" and hasattr(plugin, "detect"):
                result = await plugin.detect(infile)
                return result
            else:
                return jsonify({"error": "unsupported action"}), 400
            return None
        except PluginError as exc:
            return str(exc)

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(run())
    loop.close()
    if isinstance(result, str):
        return jsonify({"result": result})
    if result:
        return jsonify({"error": result}), 500
    return send_file(output, as_attachment=True)


if __name__ == "__main__":
    app.run(port=5000)
