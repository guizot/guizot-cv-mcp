# CV MCP Server

A Model Context Protocol (MCP) server that provides structured access to CV/resume information through various search and retrieval tools.

## Overview

This MCP server parses and serves CV data from `cv.md`, providing multiple tools to search, filter, and retrieve specific sections of professional information. Built with FastMCP, it offers both general CV access and specialized tools for work experience, skills, projects, and more.

## Features

- **Full CV Access**: Retrieve complete CV content
- **Section-based Retrieval**: Get specific CV sections (Career, Education, Skills, etc.)
- **Keyword Search**: Search across entire CV content
- **Technology Search**: Find experience and skills by specific technologies
- **Structured Data**: Extract work experience, skills, projects, and contact info
- **Health Monitoring**: Built-in health check endpoint

## Installation

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

```bash
python cv_mcp_server.py
```

The server will start and provide MCP tools for CV data access.

### Available Tools

#### General Tools
- `health()` - Health check endpoint
- `get_full_cv()` - Retrieve complete CV content
- `search_cv(keyword)` - Search CV content by keyword
- `get_all_sections()` - List all available CV sections
- `get_section_by_name(section_name)` - Get content of specific section

#### Structured Data Tools
- `get_work_experience()` - Extract structured work experience information
- `get_skills()` - Get skills organized by category
- `get_projects()` - Retrieve project information
- `get_contact_info()` - Get contact information
- `search_by_technology(technology)` - Search CV for specific technology/skill

#### Section-specific Tools
- `get_about()` - Get about section
- `get_education()` - Get education information
- `get_career()` - Get career section
- `get_career_projects()` - Get career projects section
- `get_personal_projects()` - Get personal projects section
- `get_design_projects()` - Get design projects section
- `get_achievements()` - Get achievements section
- `get_personal_journey()` - Get personal journey section
- `get_download_formats()` - Get available download formats

## Project Structure

```
├── cv_mcp_server.py    # Main MCP server implementation
├── cv.md              # CV data source (markdown format)
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## CV Data Format

The CV data is stored in `cv.md` using markdown format with specific section headers:

- `## About` - Professional summary
- `## Career` - Work experience with company details
- `## Education` - Academic background
- `## Career Projects` - Professional projects
- `## Personal Projects` - Side projects and experiments
- `## Design Projects` - UI/UX design work
- `## Skills` - Technical skills by category
- `## Achievements` - Awards and recognition
- `## Personal Journey` - Background story
- `## Contact & Links` - Contact information
- `## Available Download Formats` - CV download options

## Example Usage

```python
# Search for Python experience
results = search_by_technology("Python")

# Get structured work experience
experience = get_work_experience()

# Search CV for specific keywords
search_results = search_cv("Android")

# Get specific section
education = get_education()
```

## Dependencies

- `fastmcp` - FastMCP framework for building MCP servers
- `fastapi` - Web framework for the MCP server
- `uvicorn` - ASGI server for running FastAPI applications

## Configuration

No additional configuration required. The server reads CV data directly from `cv.md` in the same directory.

## License

This project is provided as-is for CV data management and MCP integration purposes.

---

**Note**: This MCP server is designed to work with MCP-compatible clients and provides structured access to CV data for professional and educational purposes.