# Development Container Setup Guide

This repository now includes a fully configured **VS Code Development Container** for the Smart ATS Resume project! 🎉

## What's Included

### 📦 Development Container Features

- **Python 3.11** runtime environment
- **Git** and **GitHub CLI** pre-installed
- **Automatic dependency installation** via `requirements.txt`
- **VS Code extensions** for Python development:
  - Python language support with Pylance
  - Black code formatter
  - Jupyter notebooks support
  - Ruff linter
  - GitHub Copilot (if you have access)
  - GitLens for Git visualization
  - Docker tools
  - Error Lens for better error visibility

### 🔧 Pre-configured Settings

- **Auto-formatting** with Black on save
- **Import organization** on save
- **Python linting** with Pylint
- **Pytest** test framework
- **Port forwarding** for Streamlit (8501)

### 📁 New Files Created

```
.devcontainer/
├── devcontainer.json      # Main container configuration
├── post-create.sh         # Automated setup script
└── README.md             # Container documentation

.vscode/
├── launch.json           # Debug configurations
├── tasks.json            # Build/run tasks
└── settings.json         # Workspace settings

.env.example              # Environment variables template
requirements.txt          # Python dependencies
Dockerfile               # Standalone Docker image
docker-compose.yml       # Docker Compose configuration
```

## 🚀 Quick Start

### Option 1: Using VS Code Dev Container (Recommended)

1. **Install Prerequisites:**
   - [Visual Studio Code](https://code.visualstudio.com/)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **Open in Container:**
   ```bash
   # Open VS Code in the project directory
   code .

   # Then press F1 and select:
   # "Dev Containers: Reopen in Container"
   ```

3. **Wait for Setup:**
   - First time: ~5-10 minutes (builds container, installs dependencies)
   - Subsequent times: ~30 seconds

4. **Configure API Keys:**
   - Open `.env` file (auto-created from `.env.example`)
   - Add your API keys:
     ```env
     OPENAI_API_KEY=sk-your-key-here
     SERPER_API_KEY=your-key-here
     ```

5. **Run the Application:**
   - **Web UI:** Press `Ctrl+Shift+P` → "Tasks: Run Task" → "Run Streamlit App"
   - **CLI:** Press `Ctrl+Shift+P` → "Tasks: Run Task" → "Run CLI Application"
   - Or use the integrated terminal:
     ```bash
     streamlit run streamlit_app.py
     # or
     python3 bin/crew_run.py
     ```

### Option 2: Using Docker Compose

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Run web interface
docker-compose up app

# Or run CLI (one-time)
docker-compose run --rm cli
```

### Option 3: Using Standalone Dockerfile

```bash
# Build the image
docker build -t smart-ats-resume .

# Run the container
docker run -p 8501:8501 --env-file .env smart-ats-resume
```

## 🎯 Available VS Code Tasks

Press `Ctrl+Shift+P` → "Tasks: Run Task" → Select:

- **Run Streamlit App** - Start the web interface
- **Run CLI Application** - Execute the command-line version
- **Format Code with Black** - Auto-format all Python files
- **Lint with Pylint** - Check code quality
- **Run Tests** - Execute pytest suite
- **Install Dependencies** - Update Python packages

## 🐛 Debugging

Press `F5` or use the Run and Debug panel:

- **Debug Streamlit App** - Debug the web interface
- **Debug CLI Application** - Debug the CLI script
- **Python: Current File** - Debug any open Python file
- **Python: Debug Tests** - Debug pytest tests

## 📋 Development Workflow

1. **Start the dev container** (first time only)
2. **Configure `.env`** with your API keys
3. **Make code changes** with auto-formatting and linting
4. **Run the app** using tasks or terminal
5. **Debug** using VS Code's integrated debugger
6. **Test** your changes with pytest
7. **Commit** your work

## 🔍 Key Files Explained

### `.devcontainer/devcontainer.json`
Main configuration for the development container. Defines:
- Base Docker image (Python 3.11)
- VS Code extensions to install
- Port forwarding rules
- Post-creation commands

### `.devcontainer/post-create.sh`
Automated setup script that runs after container creation:
- Upgrades pip
- Installs Python dependencies
- Creates `.env` from template
- Sets up project directories

### `requirements.txt`
Python dependencies for the project:
- **crewai** - Multi-agent AI framework
- **streamlit** - Web UI framework
- **openai** - OpenAI API client
- **chromadb** - Vector database
- Development tools (black, pylint, pytest)

### `.env.example`
Template for environment variables:
- OpenAI API key
- Serper API key
- Database configuration
- Application settings

## 🛠️ Customization

### Adding Python Packages

1. Add to `requirements.txt`:
   ```txt
   new-package>=1.0.0
   ```

2. Rebuild container:
   - Press `F1` → "Dev Containers: Rebuild Container"

   Or install directly:
   ```bash
   pip install new-package
   ```

### Changing Python Version

Edit `.devcontainer/devcontainer.json`:
```json
{
  "image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye"
}
```

### Adding VS Code Extensions

Edit `.devcontainer/devcontainer.json`:
```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "publisher.extension-id"
      ]
    }
  }
}
```

## 🔧 Troubleshooting

### Container Won't Start

1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Increase Docker resources:**
   - Docker Desktop → Settings → Resources
   - Recommended: 4GB RAM, 2 CPUs

3. **Rebuild without cache:**
   - `F1` → "Dev Containers: Rebuild Container Without Cache"

### Python Packages Not Found

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or rebuild container
# F1 → "Dev Containers: Rebuild Container"
```

### Port 8501 Already in Use

```bash
# Find and kill the process
lsof -ti:8501 | xargs kill -9

# Or change the port in devcontainer.json
"forwardPorts": [8502]
```

### API Keys Not Working

1. Verify `.env` file exists in project root
2. Check API keys format (no quotes needed)
3. Restart terminal session to reload environment

### Streamlit Won't Start

```bash
# Check if Streamlit is installed
pip show streamlit

# Reinstall if needed
pip install --force-reinstall streamlit
```

## 📚 Additional Resources

- [VS Code Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Python Best Practices](https://docs.python-guide.org/)

## 🤝 Contributing

When contributing to this project:

1. Use the dev container for consistent environment
2. Run `black .` before committing (auto-formats code)
3. Run `pylint utils/ bin/` to check code quality
4. Run `pytest` to ensure tests pass
5. Update `requirements.txt` if you add dependencies

## 📝 Notes

- The dev container mounts your SSH keys (read-only) for Git operations
- Environment variables are set to prevent Python bytecode compilation
- Auto-save and format-on-save are enabled by default
- The container user is `vscode` (non-root)

## 🎉 Enjoy Coding!

You now have a professional, fully-configured development environment for the Smart ATS Resume project. Happy coding! 🚀
