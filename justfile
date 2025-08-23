default: build

# Construct the virtual environment for building.
venv:
    python3 -m venv venv
    pip install -r requirements.txt

# Build the website starting at `root/`.
build:
