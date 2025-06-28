# Future Proposals

The following features remain on the long-term roadmap. Several earlier
proposals such as enhanced plugin adapters, progress indicators in the GUI,
automated CI and the web interface have already been implemented.

- Integrate diffusion model based video steganography.
- Build VoIP timing channel module.
- Provide HTML/JSON forensic reporting dashboard.
- Introduce dynamic plugin discovery to simplify third-party extensions.
- Package the tool using PyInstaller for easy distribution.
- Implement optional in-memory encryption for sensitive payloads.
- Provide a plugin marketplace to share community extensions.
- Incorporate an optional CLI wizard for guided setup.
- Add sample datasets and notebooks demonstrating detection workflows.

### Additional Ideas
- Create a Python API for scripted workflows and automation.
- Explore GPU-accelerated steganalysis with pre-trained models.
- Run third-party tools in lightweight containers for isolation.
- Support distributed scanning across remote workers.
- Integrate GPU acceleration for compute-intensive algorithms.
- Provide cross-platform desktop packaging for macOS and Windows.
- Add batch processing mode for entire directories with progress summaries.
- Integrate optional cloud storage backends for remote payload retrieval.
- Support external key management systems for passwordless encryption.

### New Enhancement Ideas
- Mobile-friendly web UI for scanning images on the go.
- Automatic update checker for external plugins.
- Visualization of detection results with interactive charts.
- Plugin sandboxing using subprocess isolation.

- Verify critical dependencies like `cryptography` during CI setup to avoid
  missing-package errors.
- Add optional logging plugin to track usage statistics while preserving
  user privacy through anonymization.

- Bundle Python wheel dependencies in a `vendor/` folder and provide an
  `offline_install.sh` script for air-gapped environments.
