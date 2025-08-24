default:
    just --list

# Construct the virtual environment for building.
venv:
    python3 -m venv venv
    pip install -r requirements.txt

# Build the website starting at `root/`.
build:
    source venv/bin/activate && \
    python3 build.py && \
    deactivate

# Constructs virtual environment and builds website starting at `root/`.
setup-and-build: venv build
