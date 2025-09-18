# Mars AI Agents 🚀

> Advanced Gmail integration and processing system with React frontend and FastAPI backend

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 16+](https://img.shields.io/badge/node.js-16+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-blue.svg)](https://reactjs.org/)

## 🌟 Features

- **📧 Gmail Integration** - Connects to Gmail API to download email attachments
- **🚀 FastAPI Backend** - Modern async API with automatic documentation
- **⚛️ React Frontend** - Beautiful, responsive UI with Mars-themed design
- **📄 Document Viewer** - Split-screen layout for viewing downloaded documents
- **🔐 Secure Authentication** - OAuth 2.0 with Google Gmail API
- **📁 Smart File Management** - Organized storage with date-based folders
- **🎨 Modern UI/UX** - Glassmorphism design with smooth animations

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React UI      │    │   FastAPI        │    │   Gmail API     │
│                 │◄──►│   Backend        │◄──►│                 │
│ • Processing    │    │                  │    │ • Authentication│
│ • Document View │    │ • Gmail API      │    │ • Email Search  │
│ • File Display  │    │ • File Serving   │    │ • Attachments   │
└─────────────────┘    │ • CORS Support   │    └─────────────────┘
                       └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js 16 or higher
- Gmail API credentials (see [Gmail Setup Guide](GMAIL_SETUP.md))

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd mars_AIAgents

# Install Python dependencies
pip install -r requirements.txt
# or using uv (faster)
uv pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### Setup Gmail API

1. Follow the detailed instructions in [`GMAIL_SETUP.md`](GMAIL_SETUP.md)
2. Download `credentials.json` from Google Cloud Console
3. Place it in the project root directory

### Run the Application

**Option 1: Automatic Start (Recommended)**
```bash
python start_dev.py
```

**Option 2: Manual Start**
```bash
# Terminal 1 - FastAPI Backend
python api_server.py

# Terminal 2 - React Frontend
npm start
```

**Option 3: Test Package Structure**
```bash
python test_package.py
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
mars_AIAgents/
├── 📄 README.md                    # This file
├── 📋 requirements.txt             # Python dependencies
├── 📦 package.json                 # Node.js dependencies
├── ⚙️ pyproject.toml              # Python project configuration
├── 🚫 .gitignore                   # Git ignore rules
├── 📚 GMAIL_SETUP.md              # Gmail API setup guide
├── 📖 INSTALLATION.md             # Detailed installation guide
├── 🏗️ PACKAGE_STRUCTURE.md        # Package structure documentation
├── 📊 INIT_FILES_SUMMARY.md       # __init__.py files documentation
│
├── 🐍 Python Backend/
│   ├── 📁 __init__.py              # Main package
│   ├── 🌐 api_server.py           # FastAPI backend server
│   ├── 📧 get_data.py             # Gmail API integration
│   ├── 🚀 start_dev.py            # Development launcher
│   ├── 🧪 test_package.py         # Package structure tests
│   ├── 📁 config/                 # Configuration package
│   │   └── __init__.py
│   └── 📁 utils/                  # Utilities package
│       └── __init__.py
│
├── ⚛️ React Frontend/
│   ├── 📁 src/                    # React source code
│   │   ├── 🏠 index.js           # React entry point
│   │   ├── 🎛️ ProcessingPage.jsx  # Main processing interface
│   │   ├── 📄 DocumentViewer.jsx  # Document viewing component
│   │   ├── 🎨 ProcessingPage.css  # Main styling
│   │   ├── 🎨 DocumentViewer.css  # Document viewer styling
│   │   └── 🖼️ download.jpeg       # Background image
│   ├── 📁 public/                 # Static files
│   │   └── 📄 index.html          # HTML template
│   ├── ⚙️ webpack.config.js       # Webpack configuration
│   └── 📁 dist/                   # Built files
│
├── 📁 static/                     # Static assets
├── 📁 templates/                  # Template files
└── 📁 data/                       # Downloaded attachments (gitignored)
```

## 🎯 How It Works

### 1. **Email Processing**
- User clicks "Start Processing" button
- System connects to Gmail API using OAuth 2.0
- Searches for emails from `demotest.tcs@gmail.com` with attachments
- Downloads attachments to `data/YYYY-MM-DD/` folders

### 2. **Document Viewing**
- After successful download, automatically opens document viewer
- Left panel displays the downloaded document (PDF, images, text)
- Right panel is ready for future AI analysis features
- Supports PDF viewing, image display, and text file rendering

### 3. **File Management**
- Files organized by date in separate folders
- Duplicate handling with automatic renaming
- Secure file serving through FastAPI

## 🔧 Configuration

### Gmail Settings
```python
# Default configuration in config/__init__.py
'gmail': {
    'target_email': 'demotest.tcs@gmail.com',
    'search_hours_back': 24,
    'max_results': 10,
    'credentials_file': 'credentials.json',
    'token_file': 'token.json'
}
```

### Server Settings
```python
'server': {
    'host': '0.0.0.0',
    'port': 8000,
    'reload': True,
    'log_level': 'info'
}
```

## 🧪 Testing

```bash
# Test package structure
python test_package.py

# Test individual components
python -c "import mars_AIAgents; print('✅ Package OK')"
python -c "from mars_AIAgents import config; print('✅ Config OK')"
python -c "from mars_AIAgents import utils; print('✅ Utils OK')"

# Build frontend
npm run build
```

## 📚 API Documentation

When running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints
- `POST /api/process` - Start Gmail processing
- `GET /api/status` - Get system status
- `GET /api/files` - List downloaded files
- `GET /api/config` - Get configuration
- `GET /documents/{path}` - Serve document files
- `GET /health` - Health check

## 🔒 Security

- **Never commit sensitive files**: `credentials.json`, `token.json`
- **OAuth 2.0 authentication** with Gmail API
- **Read-only Gmail access** - cannot send emails or modify content
- **CORS configured** for frontend-backend communication
- **Secure file serving** through FastAPI static files

## 🚨 Troubleshooting

### Common Issues

1. **"No module named 'mars_AIAgents'"**
   ```bash
   # Run from parent directory
   cd /path/to/parent
   python mars_AIAgents/test_package.py
   ```

2. **"credentials.json not found"**
   - Follow [Gmail Setup Guide](GMAIL_SETUP.md)
   - Ensure file is in project root

3. **"Port already in use"**
   ```bash
   # Kill processes on ports 3000 and 8000
   kill -9 $(lsof -t -i :3000)
   kill -9 $(lsof -t -i :8000)
   ```

4. **"No new emails found"**
   - Send test email with attachment from `demotest.tcs@gmail.com`
   - Check date range (default: last 24 hours)

## 🛠️ Development

### Adding New Features

1. **New Utility Functions**
   ```bash
   # Create: utils/new_feature.py
   # Update: utils/__init__.py
   ```

2. **New Configuration**
   ```bash
   # Update: config/__init__.py
   # Add new settings to DEFAULT_CONFIG
   ```

3. **New API Endpoints**
   ```bash
   # Update: api_server.py
   # Add new FastAPI routes
   ```

### Code Style
- Python: Follow PEP 8
- JavaScript: Use ES6+ features
- CSS: BEM methodology recommended

## 📈 Future Enhancements

- 🤖 **AI Document Analysis** - Integration with LLMs for content analysis
- 📊 **Document Processing** - Text extraction and data parsing
- 🔍 **Search Functionality** - Full-text search across documents
- 📧 **Multi-Email Support** - Process emails from multiple accounts
- 🗄️ **Database Integration** - Store metadata and processing results
- 📱 **Mobile Support** - Responsive design improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Gmail API** for email integration capabilities
- **FastAPI** for the excellent async web framework
- **React** for the powerful frontend framework
- **Google Cloud Console** for API management

## 📞 Support

For issues and questions:
1. Check the [troubleshooting section](#-troubleshooting)
2. Review the documentation files
3. Open an issue on GitHub

---

**Mars AI Agents** - Bridging the gap between email communication and intelligent document processing 🚀