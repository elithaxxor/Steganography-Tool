from __future__ import annotations

import asyncio
from pathlib import Path

from flask import Flask, jsonify, request, send_file

from stego_plugins import OutGuess, PluginError

app = Flask(__name__)


@app.post("/api/v3/plugin/<tool>/<action>")
def plugin_route(tool: str, action: str):
    args = request.json or {}
    infile = Path(args.get("infile", ""))
    payload = Path(args.get("payload", "")) if args.get("payload") else None
    output = Path(args.get("output", "output.bin"))

    if tool != "outguess":
        return jsonify({"error": "unsupported tool"}), 400

    try:
        plugin = OutGuess()
    except PluginError as exc:
        return jsonify({"error": str(exc)}), 500

    async def run():
        try:
            if action == "embed":
                await plugin.embed(infile, payload, output)
            elif action == "extract":
                await plugin.extract(infile, output)
            else:
                return jsonify({"error": "unsupported action"}), 400
            return None
        except PluginError as exc:
            return str(exc)

    loop = asyncio.new_event_loop()
    err = loop.run_until_complete(run())
    loop.close()
    if err:
        return jsonify({"error": err}), 500
    return send_file(output, as_attachment=True)


if __name__ == "__main__":
    app.run(port=5000)
