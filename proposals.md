# Future Proposals

The following features remain on the long-term roadmap. Several earlier
proposals such as enhanced plugin adapters, progress indicators in the GUI,
automated CI and the web interface have already been implemented.

- Integrate diffusion model based video steganography.
- Build VoIP timing channel module.
- Provide HTML/JSON forensic reporting dashboard.
- Introduce dynamic plugin discovery to simplify third-party extensions.
- Enhance the GUI with theming support and advanced scan configuration panels.
- Package the tool using PyInstaller for easy distribution. Milestone: produce standalone executables for Windows, macOS, and Linux.
- Implement optional in-memory encryption for sensitive payloads.
- Provide a plugin marketplace to share community extensions.
- Incorporate an optional CLI wizard for guided setup.
- Add sample datasets and notebooks demonstrating detection workflows.

### Additional Ideas
- Create a Python API for scripted workflows and automation.
- Explore GPU-accelerated steganalysis with pre-trained models.
- Run third-party tools in lightweight containers for isolation. Milestone: publish official Docker images for the CLI and web interface.
- Support distributed scanning across remote workers. Milestone: coordinate jobs via a message queue and aggregate results from each node.
- Integrate GPU acceleration for compute-intensive algorithms. Milestone: prototype CUDA kernels for deep steganalysis models.
- Provide cross-platform desktop packaging for macOS and Windows.
- Provide a Dockerized setup of the entire tool for quick testing and deployment.
- Add batch processing mode for entire directories with progress summaries.
- Integrate optional cloud storage backends for remote payload retrieval.
- Support external key management systems for passwordless encryption.

### New Enhancement Ideas
- Mobile-friendly web UI for scanning images on the go.
- Automatic update checker for external plugins.
- Visualization of detection results with interactive charts.
- Plugin sandboxing using subprocess isolation.

- Bundle Python wheel dependencies in a `vendor/` folder and provide an
  `offline_install.sh` script for air-gapped environments.
