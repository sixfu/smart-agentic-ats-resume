# Development Container for Smart ATS Resume

This development container provides a fully configured Python environment for the Smart ATS Resume project.

## Features

- **Python 3.11** runtime environment
- **Pre-installed extensions**:
  - Python language support
  - Pylance for IntelliSense
  - Black formatter
  - Jupyter notebooks support
  - Ruff linter
  - GitHub Copilot
  - GitLens
  - Docker tools
  - Error Lens

- **Pre-configured settings**:
  - Auto-formatting on save with Black
  - Import organization on save
  - Python linting with Pylint
  - Pytest test framework

- **Port forwarding**:
  - Port 8501 for Streamlit web interface

## Getting Started

### 1. Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### 2. Open in Container

1. Open this project folder in VS Code
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Select "Dev Containers: Reopen in Container"
4. Wait for the container to build (first time only, ~5-10 minutes)

### 3. Configure API Keys

After the container starts:

1. Open the `.env` file (created from `.env.example`)
2. Add your API keys:
   ```env
   OPENAI_API_KEY=sk-...
   SERPER_API_KEY=...
   ```

### 4. Run the Application

#### Web Interface (Streamlit)
```bash
streamlit run streamlit_app.py
```
The app will be available at `http://localhost:8501`

#### CLI Interface
```bash
python3 bin/crew_run.py
```

## Directory Structure

```
.devcontainer/
├── devcontainer.json      # Container configuration
├── post-create.sh         # Setup script (runs after container creation)
└── README.md             # This file
```

## Customization

### Adding Python Packages

1. Add the package to `requirements.txt`
2. Rebuild the container:
   - Press `F1` → "Dev Containers: Rebuild Container"

Or install directly in the terminal:
```bash
pip install package-name
```

### Modifying Container Settings

Edit `.devcontainer/devcontainer.json` to:
- Change Python version (modify `image` field)
- Add VS Code extensions
- Configure ports
- Add environment variables

### Post-Creation Commands

Edit `.devcontainer/post-create.sh` to add custom setup steps that run after container creation.

## Troubleshooting

### Container won't start
- Ensure Docker Desktop is running
- Check Docker has enough resources (Settings → Resources)
- Try: "Dev Containers: Rebuild Container Without Cache"

### Python packages not found
- Rebuild container: `F1` → "Dev Containers: Rebuild Container"
- Or manually install: `pip install -r requirements.txt`

### Port 8501 already in use
- Stop other Streamlit instances
- Or change the port in `devcontainer.json` and restart

### API keys not working
- Verify `.env` file exists in project root
- Check API keys are correctly formatted
- Restart the terminal session

## Resources

- [VS Code Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
