# Mars AI Agents - Installation Guide

Complete setup instructions for the Mars AI Agents Gmail processing system.

## Prerequisites

- **Python 3.10 or higher**
- **Node.js 16 or higher** 
- **npm or yarn**
- **Gmail account** for testing
- **Google Cloud Console** access for Gmail API setup

## Installation Methods

### Method 1: Using requirements.txt (Recommended)

```bash
# Clone or navigate to project directory
cd /Users/anirudh/Downloads/Mars_Project/mars_AIAgents

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### Method 2: Using pyproject.toml

```bash
# Install project in editable mode
pip install -e .

# Install Node.js dependencies
npm install
```

### Method 3: Minimal Installation

```bash
# Install only core dependencies
pip install -r requirements-minimal.txt

# Install Node.js dependencies
npm install
```

## Verification

### Check Python Dependencies
```bash
python -c "import fastapi, google.auth, googleapiclient; print('✅ All Python dependencies installed')"
```

### Check Node.js Dependencies
```bash
npm list --depth=0
```

### Test FastAPI Server
```bash
python api_server.py
# Should start on http://localhost:8000
# Visit http://localhost:8000/docs for API documentation
```

### Test React Application
```bash
npm start
# Should start on http://localhost:3000
```

## Gmail API Setup

**Important**: The system requires Gmail API credentials to function.

1. **Follow the detailed instructions in `GMAIL_SETUP.md`**
2. **Download `credentials.json` from Google Cloud Console**
3. **Place it in the project root directory**

## Quick Start

### Option 1: Automated Start
```bash
python start_dev.py
```

### Option 2: Manual Start
```bash
# Terminal 1 - FastAPI Backend
python api_server.py

# Terminal 2 - React Frontend  
npm start
```

## Project Structure After Installation

```
mars_AIAgents/
├── node_modules/           # Node.js dependencies
├── venv/                   # Python virtual environment (if created)
├── src/                    # React source code
├── data/                   # Downloaded email attachments
├── credentials.json        # Gmail API credentials (you need to add this)
├── token.json             # OAuth token (auto-generated)
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
└── ...
```

## Environment Configuration

### Optional: Create .env file
```bash
# Create .env file for environment variables
cat > .env << EOF
# FastAPI Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_RELOAD=true

# Gmail Configuration
GMAIL_TARGET_EMAIL=demotest.tcs@gmail.com
GMAIL_SEARCH_HOURS=24
GMAIL_MAX_RESULTS=10

# Development
DEBUG=true
LOG_LEVEL=info
EOF
```

## Troubleshooting

### Common Installation Issues

#### Python Dependencies
```bash
# If pip install fails, try upgrading pip
python -m pip install --upgrade pip

# If you get permission errors on macOS
pip install --user -r requirements.txt
```

#### Node.js Dependencies
```bash
# Clear npm cache if installation fails
npm cache clean --force

# Try using different cache location
npm install --cache /tmp/.npm
```

#### Port Conflicts
```bash
# Check if ports are in use
lsof -i :3000  # React dev server
lsof -i :8000  # FastAPI server

# Kill processes if needed
kill -9 $(lsof -t -i :3000)
kill -9 $(lsof -t -i :8000)
```

#### Gmail API Issues
- Ensure `credentials.json` exists in project root
- Check Google Cloud Console for API quotas
- Verify OAuth consent screen configuration
- Add your Gmail account as a test user

### Version Compatibility

#### Python Versions
- **Minimum**: Python 3.10
- **Recommended**: Python 3.11 or 3.12
- **Tested**: Python 3.12

#### Node.js Versions  
- **Minimum**: Node.js 16
- **Recommended**: Node.js 18 or 20 LTS
- **Tested**: Node.js 20

## Development Setup

### Install Development Dependencies
```bash
# Python development tools
pip install -r requirements.txt
pip install pytest black isort flake8

# Or using pyproject.toml
pip install -e ".[dev]"
```

### Code Formatting
```bash
# Format Python code
black .
isort .

# Lint Python code  
flake8 .

# Run tests
pytest
```

## Production Deployment

### Python Backend
```bash
# Install production dependencies only
pip install --no-dev -r requirements.txt

# Run with production ASGI server
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### React Frontend
```bash
# Build for production
npm run build

# Serve built files (you'll need a web server)
```

## Support

- **Gmail API Setup**: See `GMAIL_SETUP.md`
- **API Documentation**: http://localhost:8000/docs (when server is running)
- **React Documentation**: Standard Create React App structure

## Security Notes

- **Never commit** `credentials.json` or `token.json` to version control
- **Use environment variables** for sensitive configuration in production
- **Enable firewall rules** for production deployments
- **Consider service accounts** for production Gmail API access