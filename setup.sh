# Install Tools
echo "INFO: Installing Tools (Homebrew)"
brew install uv

# Setup Python Virtual Environment
echo -e
echo "INFO: Creating Python Virtual Environment"
uv venv .venv --python 3.14 --clear
echo -e
echo "INFO: Activating Python Virtual Environment"
source .venv/bin/activate

# Download Project Libraries
echo -e
echo "INFO: Installing Libraries"
# uv pip install -e . # install deps in pyproject.toml
uv sync
echo "INFO: Python Version: $(python --version)"
echo "INFO: uv Version: $(uv --version)"
