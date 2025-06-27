# Changelog

## [Unreleased]
### Added
- Basic plugin framework under `stego_plugins` with OutGuess adapter.
- `stego.py` CLI with plugin command.
- Minimal Flask API (`api.py`) exposing `/api/v3/plugin/<tool>/<action>`.
- Pytest unit test for missing OutGuess binary.
- Requirements update and setup script.
