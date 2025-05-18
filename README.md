<h1 align="center"> Final Exam Cloud Comp </h1>
<h3 align="center"><a href="https://final-exam-cloud-comp-streamlit.onrender.com">Streamlit App</a><h3>

# Repository Structure
```bash
my-project/
├── .streamlit/
│   ├── config.toml        # Streamlit customization
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
├── pyproject.toml         # Dependency management (preferred)
├── requirements.txt       # Dependency management (old school)  
├── dashboard.py           # Streamlit app
└── main.py                # CLI Tools
```

# Prerequisites
Install uv
```bash
pip install uv
```

# Setup
Install dependencies. This creates a `.venv` in the same repo. Use this `.venv` to run notebooks.
```bash
uv sync
```
Add a dependency. This adds a dependency to `pyproject.toml` and install it in the `.venv`.
```bash
uv add <package_name>
```

# Command Line Tools

**How to use:**
`uv run` runs python scripts and tools using the packages/libraries in `.venv`.
```bash
uv run main.py <command>
```

**With options (Python scripts):**
```bash
uv run main.py <command> --<option> <option_value>
```

Example: `uv run main.py start-streamlit --port 10000`

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

## Streamlit Commands

| Command        | Options | Description |
|----------------|--------|-------------|
| start-streamlit| port: int = 8501, host: str = "0.0.0.0" | Start the Streamlit dashboard |
