## Disneyland Reviews Explorer (Python Coursework Project)

This project provides a simple text-based interface for exploring a dataset of
Disneyland reviews stored in `data/disneyland_reviews.csv`.  It is organised
into clear modules to separate responsibilities:

- **`main.py`**: overall program flow and orchestration
- **`tui.py`**: all user input and output (Text User Interface)
- **`process.py`**: data loading and processing
- **`visual.py`**: visualisations using Matplotlib

### Running the program

1. **Create and activate a virtual environment** (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Run the program** from the project root (the same folder as `main.py`):

```bash
python main.py
```

### Features

- Load and summarise the Disneyland reviews dataset
- View average ratings by branch
- View average ratings by year-month for a specific branch
- View the most common reviewer locations for a branch
- Plot these aggregates using Matplotlib (if installed)

All user interaction happens in the terminal via a simple menu.

