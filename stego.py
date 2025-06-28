#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import argparse
from pathlib import Path

from stego_plugins import discover_plugins, reload_plugins, PluginError
from tqdm import tqdm


async def run_with_progress(coro: asyncio.Future, desc: str) -> str:
    """Display a simple progress bar while awaiting a coroutine."""
    task = asyncio.create_task(coro)
    with tqdm(total=100, desc=desc) as prog:
        while not task.done():
            await asyncio.sleep(0.1)
            prog.update(1)
            if prog.n >= 100:
                prog.n = 0
                prog.refresh()
        prog.update(100 - prog.n)
    return await task

PLUGIN_MAP = discover_plugins()


async def run_plugin(args: argparse.Namespace) -> None:
    tool = args.tool
    action = args.action

    plugin_cls = PLUGIN_MAP.get(tool)
    if not plugin_cls:
        # try reloading in case new plugins were installed
        PLUGIN_MAP.update(reload_plugins())
        plugin_cls = PLUGIN_MAP.get(tool)
        if not plugin_cls:
            raise SystemExit(f"Unsupported tool: {tool}")
    plugin = plugin_cls()

    try:
        if action == "embed":
            await run_with_progress(
                plugin.embed(Path(args.infile), Path(args.payload), Path(args.output)),
                f"{tool} embed",
            )
            print("Embed successful")
        elif action == "extract":
            await run_with_progress(
                plugin.extract(Path(args.infile), Path(args.output)),
                f"{tool} extract",
            )
            print("Extraction successful")
        elif action == "detect" and hasattr(plugin, "detect"):
            result = await run_with_progress(
                plugin.detect(Path(args.infile)), f"{tool} detect"
            )
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
