# Optimize Crossword

A crossword puzzle generator using Mixed Integer Programming (MIP) and adhering to SOLID software engineering principles.

## Features

- Generate crosswords with arbitrary shapes and sizes.
- Plugin system for crossword generation algorithms.
- Configurable output handlers (print, HTTP).
- Uses `pulp` for solving MIP problems.
- Configurable via YAML files.

## Installation

Clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/yourusername/optimize_crossword.git
cd optimize_crossword
poetry install
