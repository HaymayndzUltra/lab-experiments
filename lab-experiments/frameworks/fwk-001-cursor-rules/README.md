# Cursor Rules Framework

A framework for managing and applying coding rules in Cursor IDE. This framework provides utilities for creating, validating, and applying coding standards and best practices across development projects.

## What is this?

The Cursor Rules Framework is a Python-based tool that helps developers enforce coding standards by:
- Defining custom rules for code quality
- Validating source files against these rules
- Providing a flexible engine for rule processing
- Supporting different severity levels (error, warning, info)

## Quick Run

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
# Clone or navigate to the framework directory
cd frameworks/fwk-001-cursor-rules

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage
```bash
# Run the example
python examples/basic_usage.py

# Run tests
python -m pytest tests/

# Or run tests directly
python tests/test_core.py
```

### Docker
```bash
# Build the image
docker build -t cursor-rules .

# Run the container
docker run cursor-rules
```

## Project Structure

```
├─ src/                   # Core framework code
│  ├─ __init__.py        # Package initialization
│  └─ core.py            # Main rules engine
├─ tests/                 # Test suite
│  └─ test_core.py       # Core functionality tests
├─ examples/              # Usage examples
│  └─ basic_usage.py     # Basic framework usage
├─ Dockerfile             # Container configuration
├─ README.md              # This file
├─ LAB_NOTES.md           # Development decisions and notes
└─ requirements.txt       # Python dependencies
```

## Core Components

- **Rule**: Data class representing a single coding rule
- **CursorRulesEngine**: Main engine for processing and applying rules
- **File Validation**: Scan files for rule violations
- **Configurable Severity**: Error, warning, and info levels

## Example Rules

- Find TODO comments in code
- Detect print statements (suggest logging instead)
- Identify hardcoded passwords
- Custom pattern matching for any coding standard

## Contributing

See `LAB_NOTES.md` for development decisions, risks, and next steps.
