# Development Guide

This guide provides step-by-step instructions for setting up the development environment and running tests for the Smart CV Filter system.

## 🚀 Setup Instructions

### Prerequisites

Ensure you have the following installed:
- **Python** (3.10 or higher)
- **pip** (Python package manager)
- **venv** (Python virtual environment)
- **Git**

### 1. Clone the Repository

```bash
git clone git@github.com:LIDR-academy/smart-cv-filter.git
cd smart-cv-filter
```

### 2. Virtual Environment Setup

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On Unix or MacOS
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip to the latest version
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root for configuration:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Additional configuration can be added here
```

### 5. Backend Setup

```bash
# Navigate to backend directory
cd src/backend

# Run database migrations (if applicable)
# python manage.py migrate

# Start the development server
python main.py
```

### 6. Testing

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src

# Run specific test module
python -m pytest tests/test_extractor.py
```

### 7. Code Quality Checks

```bash
# Run type checking
mypy src

# Run linter
flake8 src

# Run code formatter
black src
```

## 🧪 Testing Strategies

### Unit Testing
- Use `pytest` for unit tests
- Place test files in `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names

### Integration Testing
- Test interactions between modules
- Verify data flow and processing logic
- Mock external dependencies (e.g., Gemini API)

### Coverage Requirements
- Aim for > 80% code coverage
- Focus on critical path and edge cases

## 🚢 Deployment Considerations

- Use virtual environments in production
- Set up proper logging and error tracking
- Secure API keys and sensitive configuration
- Consider containerization with Docker for consistent environments

## 📝 Development Workflow

1. Create a feature branch
2. Implement changes
3. Write/update tests
4. Run code quality checks
5. Commit with descriptive messages
6. Create pull request
7. Request code review

## 🔒 Security Guidelines

- Never commit sensitive information to version control
- Use environment variables for configuration
- Implement proper error handling
- Sanitize and validate all inputs
- Follow GDPR and data protection guidelines

## 📚 Additional Resources

- Python Style Guide: [PEP 8](https://peps.python.org/pep-0008/)
- Testing Framework: [pytest documentation](https://docs.pytest.org/)
- Type Checking: [mypy documentation](https://mypy.readthedocs.io/)
