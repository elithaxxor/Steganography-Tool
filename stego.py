#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import argparse
from pathlib import Path

from stego_plugins import OutGuess, StegHide, Zsteg, StegExpose, PluginError


async def run_plugin(args: argparse.Namespace) -> None:
    tool = args.tool
    action = args.action

    if tool == "outguess":
        plugin = OutGuess()
    elif tool == "steghide":
        plugin = StegHide()
    elif tool == "zsteg":
        plugin = Zsteg()
    elif tool == "stegexpose":
        plugin = StegExpose()
    else:
        raise SystemExit(f"Unsupported tool: {tool}")

    try:
        if action == "embed":
            await plugin.embed(Path(args.infile), Path(args.payload), Path(args.output))
            print("Embed successful")
        elif action == "extract":
            await plugin.extract(Path(args.infile), Path(args.output))
            print("Extraction successful")
        elif action == "detect" and hasattr(plugin, "detect"):
            result = await plugin.detect(Path(args.infile))
            print(result)
        else:
            raise SystemExit(f"Unsupported action: {action}")
    except PluginError as exc:
        print(f"Error: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Steganography Tool")
    subparsers = parser.add_subparsers(dest="command")

    plugin_parser = subparsers.add_parser("plugin", help="Run external stego tools")
    plugin_parser.add_argument("--tool", required=True, help="Tool name")
    plugin_parser.add_argument("--action", required=True, choices=["embed", "extract", "detect"])
    plugin_parser.add_argument(
        "-i", "--infile", required=True, help="Input carrier file"
    )
    plugin_parser.add_argument("-p", "--payload", help="Payload file for embed")
    plugin_parser.add_argument("-o", "--output", required=True, help="Output file")

    args = parser.parse_args()
    if args.command == "plugin":
        asyncio.run(run_plugin(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
