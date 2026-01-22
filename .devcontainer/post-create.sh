#!/bin/bash
set -e

echo "🚀 Setting up Smart ATS Resume development environment..."

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "⚠️  No requirements.txt found. Installing common dependencies..."
    pip install \
        crewai \
        crewai-tools \
        streamlit \
        python-dotenv \
        PyPDF2 \
        python-docx \
        sqlalchemy \
        chromadb \
        openai
fi

# Install development tools
echo "🛠️  Installing development tools..."
pip install \
    black \
    pylint \
    pytest \
    pytest-cov \
    ipykernel

# Create .env.example if it doesn't exist
if [ ! -f .env.example ]; then
    echo "📝 Creating .env.example template..."
    cat > .env.example << 'EOF'
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4-turbo

# Serper API for web search
SERPER_API_KEY=your_serper_api_key_here

# Optional: Database configuration
DATABASE_URL=sqlite:///./utils/db/chroma.sqlite3
EOF
fi

# Copy .env.example to .env if .env doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual API keys!"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data
mkdir -p outputs
mkdir -p utils/db

# Set up git hooks (optional)
if [ -d .git ]; then
    echo "🔧 Setting up git hooks..."
    git config core.hooksPath .devcontainer/hooks
fi

# Display helpful information
echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "📚 Quick Start Commands:"
echo "  • Run web interface:    streamlit run streamlit_app.py"
echo "  • Run CLI:             python3 bin/crew_run.py"
echo "  • Run tests:           pytest"
echo "  • Format code:         black ."
echo "  • Lint code:           pylint utils/ bin/"
echo ""
echo "⚠️  Don't forget to:"
echo "  1. Update .env with your API keys (OPENAI_API_KEY, SERPER_API_KEY)"
echo "  2. Place your resume PDF in the data/ directory"
echo ""
echo "🎉 Happy coding!"
