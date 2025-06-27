# Changelog

## [Unreleased]
### Added
- Basic plugin framework under `stego_plugins` with OutGuess adapter.
- Plugin adapters for StegHide, Zsteg and StegExpose.
- Extended CLI/API to support new plugins and detection action.
- Advanced detection pane in GUI with progress indicators.
- `stego.py` CLI with plugin command.
- Minimal Flask API (`api.py`) exposing `/api/v3/plugin/<tool>/<action>`.
- Pytest unit test for missing OutGuess binary.
- Additional unit tests for new plugins.
- Requirements update and setup script.

## [4.0] - 2024-04-30
### Added
- Aletheia and STEG-Detector machine learning detection plugins.
- Audio LSB steganography module.
- AES-GCM watermarking plugin.
- Network covert channel support (HTTP headers & DNS queries).
- Unified plugin loader used by CLI and REST API.
- Tests for new plugins and audio embedding.
