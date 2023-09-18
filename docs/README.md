# Documentation Overiview

## Repository Folder Structure

- `docs/` - Documentation (*you are here!*)

## Local Development Installation

Make sure you have the following dependencies installed on your system:

- `git`
- [Docker](https://docs.docker.com/engine/install/)
- [Python 3.10](https://www.python.org/downloads/release/python-3100/) or higher (if you do not wish to use docker)

Then run:
```bash
git clone https://github.com/CGBassPlayer/seedtuber.git
cd seedtuber

# Run with docker compose
docker compose -f docker-compose.dev.yml up
docker-compose -f docker-compose.dev.yml up # Old syntax

# OR run locally
python3 main.py
```
