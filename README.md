<h1 align="center"> Final Exam Cloud Comp </h1>

# Repository Structure
```bash
my-project/
├── data/               
│   ├── external/          # External Data
|  ...                      
│   └── processed/
├── notebooks/             # Jupyter notebooks for exploration
├── src/                   # Source code
│   ├── __init__.py
│   ├── config/            # Environment variables setup
│   ├── utils/             # Utility functions
│   └── data/
│       ├── datastorage.py # Base "data storage" class
│       ├── staging.py     # Staging functionalities class
│       └── warehouse.py   # Warehouse functionalities class
└── main.py                # CLI Tools
```

# Prerequisites
Install uv
```bash
pip install uv
```

# Setup
Install dependencies
```bash
uv sync
```

# Command Line Tools

How to use:
```bash
uv run main.py <command>
```

## Staging Commands

| Command        | Description |
|----------------|-------------|
| move-to-staging| Move the raw data to a staging database |
| read-staging   | Print table names, and column details to the terminal |
| drop-staging   | Drop every table in the staging database |

## Warehouse Commands

| Command        | Description |
|----------------|-------------|
| move-to-data-warehouse | Preprocess staging data and move to data warehouse |
| read-warehouse   | Print table names, and column details to the terminal |
| drop-warehouse   | Drop every table in the data warehouse |
