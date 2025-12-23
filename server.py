from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
import re
from typing import Dict, List, Any

# --------------------------------------------------
# Initialize MCP
# --------------------------------------------------
mcp = FastMCP(
    "cv-mcp",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["localhost:*", "127.0.0.1:*", "guizot-cv-mcp-production.up.railway.app:*"],
        allowed_origins=["http://localhost:*", "https://guizot-cv-mcp-production.up.railway.app:*"],
    )
)

# --------------------------------------------------
# Load CV (markdown only)
# --------------------------------------------------
CV_TEXT = Path("cv.md").read_text(encoding="utf-8")

# --------------------------------------------------
# Helper functions for CV parsing
# --------------------------------------------------
def parse_cv_sections() -> Dict[str, str]:
    """Parse CV into sections"""
    sections = {}
    current_section = ""
    current_content = []
    
    lines = CV_TEXT.splitlines()
    for line in lines:
        if line.startswith("## "):
            # Save previous section
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            
            # Start new section
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()
    
    return sections

def extract_work_experience() -> List[Dict[str, Any]]:
    """Extract work experience information"""
    sections = parse_cv_sections()
    career_section = sections.get("Career", "")
    
    experiences = []
    current_exp = {}
    
    lines = career_section.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("### "):
            # New position
            if current_exp:
                experiences.append(current_exp)
            current_exp = {"title": line[4:].strip()}
        elif line.startswith("**") and line.endswith("**") and not line.startswith("**Key Responsibilities:**") and not line.startswith("**Tech Stack:**"):
            # Company name (but not Key Responsibilities or Tech Stack)
            current_exp["company"] = line[2:-2].strip()
        elif line.startswith("- **Duration:**"):
            current_exp["duration"] = line.replace("- **Duration:**", "").strip()
        elif line.startswith("- **Location:**"):
            current_exp["location"] = line.replace("- **Location:**", "").strip()
        elif line.startswith("**Tech Stack:**"):
            current_exp["tech_stack"] = line.replace("**Tech Stack:**", "").strip()
    
    # Add last experience
    if current_exp:
        experiences.append(current_exp)
    
    return experiences

def extract_skills() -> Dict[str, List[str]]:
    """Extract skills by category"""
    sections = parse_cv_sections()
    skills_section = sections.get("Skills", "")
    
    skills = {}
    current_category = ""
    
    lines = skills_section.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("### "):
            current_category = line[4:].strip()
            skills[current_category] = []
        elif line and not line.startswith("#") and current_category:
            # Split by comma and clean up
            skill_list = [skill.strip() for skill in line.split(",")]
            skills[current_category].extend(skill_list)
    
    return skills

def extract_projects() -> List[Dict[str, Any]]:
    """Extract project information"""
    sections = parse_cv_sections()
    projects_section = sections.get("Career Projects", "")
    
    projects = []
    current_project = {}
    
    lines = projects_section.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("### "):
            # New project
            if current_project:
                projects.append(current_project)
            current_project = {"name": line[4:].strip()}
        elif line.startswith("**Organization:**"):
            current_project["organization"] = line.replace("**Organization:**", "").strip()
        elif line.startswith("**Link:**"):
            link_text = line.replace("**Link:**", "").strip()
            if "[Play Store]" in link_text:
                current_project["play_store"] = link_text.split("](")[1][:-1]
            elif "[Live Site]" in link_text:
                current_project["live_site"] = link_text.split("](")[1][:-1]
            else:
                current_project["link"] = link_text
    
    # Add last project
    if current_project:
        projects.append(current_project)
    
    return projects

def extract_contact_info() -> Dict[str, str]:
    """Extract contact information"""
    sections = parse_cv_sections()
    contact_section = sections.get("Contact & Links", "")
    
    contact_info = {}
    
    lines = contact_section.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("- **Email:**"):
            contact_info["email"] = line.replace("- **Email:**", "").strip()
        elif line.startswith("- **WhatsApp:**"):
            contact_info["whatsapp"] = line.replace("- **WhatsApp:**", "").strip()
        elif line.startswith("- **LinkedIn:**"):
            contact_info["linkedin"] = line.replace("- **LinkedIn:**", "").strip()
        elif line.startswith("- **GitHub:**"):
            contact_info["github"] = line.replace("- **GitHub:**", "").strip()
        elif line.startswith("- **Location:**"):
            contact_info["location"] = line.replace("- **Location:**", "").strip()
    
    return contact_info

# --------------------------------------------------
# MCP tools (NO AUTH)
# --------------------------------------------------
@mcp.tool()
def health() -> str:
    """Health check"""
    return "ok"

@mcp.tool()
def get_full_cv() -> str:
    """Return full CV"""
    return CV_TEXT

@mcp.tool()
def search_cv(keyword: str) -> str:
    """Keyword search in CV"""
    results = [
        line
        for line in CV_TEXT.splitlines()
        if keyword.lower() in line.lower()
    ]
    return "\n".join(results) if results else "No results found"

@mcp.tool()
def get_work_experience() -> str:
    """Get structured work experience information"""
    experiences = extract_work_experience()
    if not experiences:
        return "No work experience found"
    
    result = "## Work Experience\n\n"
    for exp in experiences:
        result += f"**{exp.get('title', 'Unknown Title')}**\n"
        result += f"Company: {exp.get('company', 'Unknown')}\n"
        result += f"Duration: {exp.get('duration', 'Unknown')}\n"
        result += f"Location: {exp.get('location', 'Unknown')}\n"
        if 'tech_stack' in exp:
            result += f"Tech Stack: {exp['tech_stack']}\n"
        result += "\n"
    
    return result

@mcp.tool()
def get_skills() -> str:
    """Get skills organized by category"""
    skills = extract_skills()
    if not skills:
        return "No skills found"
    
    result = "## Skills\n\n"
    for category, skill_list in skills.items():
        result += f"**{category}:**\n"
        result += ", ".join(skill_list) + "\n\n"
    
    return result

@mcp.tool()
def get_projects() -> str:
    """Get project information"""
    projects = extract_projects()
    if not projects:
        return "No projects found"
    
    result = "## Projects\n\n"
    for project in projects:
        result += f"**{project.get('name', 'Unknown Project')}**\n"
        if 'organization' in project:
            result += f"Organization: {project['organization']}\n"
        if 'play_store' in project:
            result += f"Play Store: {project['play_store']}\n"
        if 'live_site' in project:
            result += f"Live Site: {project['live_site']}\n"
        if 'link' in project:
            result += f"Link: {project['link']}\n"
        result += "\n"
    
    return result

@mcp.tool()
def get_contact_info() -> str:
    """Get contact information"""
    contact_info = extract_contact_info()
    if not contact_info:
        return "No contact information found"
    
    result = "## Contact Information\n\n"
    for key, value in contact_info.items():
        result += f"**{key.title()}:** {value}\n"
    
    return result

@mcp.tool()
def search_by_technology(technology: str) -> str:
    """Search CV for specific technology or skill"""
    tech_lower = technology.lower()
    results = []
    
    # Search in work experience
    experiences = extract_work_experience()
    for exp in experiences:
        if 'tech_stack' in exp and tech_lower in exp['tech_stack'].lower():
            results.append(f"**{exp.get('title', 'Unknown')}** at {exp.get('company', 'Unknown')}")
    
    # Search in skills
    skills = extract_skills()
    for category, skill_list in skills.items():
        for skill in skill_list:
            if tech_lower in skill.lower():
                results.append(f"**{category}:** {skill}")
    
    # Search in general CV text
    cv_results = [
        line.strip()
        for line in CV_TEXT.splitlines()
        if tech_lower in line.lower() and line.strip()
    ]
    
    if cv_results:
        results.append("\n**Other mentions:**")
        results.extend(cv_results[:10])  # Limit to first 10 results
    
    return "\n".join(results) if results else f"No mentions of '{technology}' found"

@mcp.tool()
def get_education() -> str:
    """Get education information"""
    sections = parse_cv_sections()
    education_section = sections.get("Education", "")
    
    if not education_section:
        return "No education information found"
    
    return f"## Education\n\n{education_section}"

@mcp.tool()
def get_about() -> str:
    """Get about section"""
    sections = parse_cv_sections()
    about_section = sections.get("About", "")
    
    if not about_section:
        return "No about information found"
    
    return f"## About\n\n{about_section}"

@mcp.tool()
def get_career() -> str:
    """Get career section"""
    sections = parse_cv_sections()
    career_section = sections.get("Career", "")
    
    if not career_section:
        return "No career information found"
    
    return f"## Career\n\n{career_section}"

@mcp.tool()
def get_career_projects() -> str:
    """Get career projects section"""
    sections = parse_cv_sections()
    projects_section = sections.get("Career Projects", "")
    
    if not projects_section:
        return "No career projects found"
    
    return f"## Career Projects\n\n{projects_section}"

@mcp.tool()
def get_personal_projects() -> str:
    """Get personal projects section"""
    sections = parse_cv_sections()
    projects_section = sections.get("Personal Projects", "")
    
    if not projects_section:
        return "No personal projects found"
    
    return f"## Personal Projects\n\n{projects_section}"

@mcp.tool()
def get_design_projects() -> str:
    """Get design projects section"""
    sections = parse_cv_sections()
    design_section = sections.get("Design Projects", "")
    
    if not design_section:
        return "No design projects found"
    
    return f"## Design Projects\n\n{design_section}"

@mcp.tool()
def get_achievements() -> str:
    """Get achievements section"""
    sections = parse_cv_sections()
    achievements_section = sections.get("Achievements", "")
    
    if not achievements_section:
        return "No achievements found"
    
    return f"## Achievements\n\n{achievements_section}"

@mcp.tool()
def get_personal_journey() -> str:
    """Get personal journey section"""
    sections = parse_cv_sections()
    journey_section = sections.get("Personal Journey", "")
    
    if not journey_section:
        return "No personal journey found"
    
    return f"## Personal Journey\n\n{journey_section}"

@mcp.tool()
def get_download_formats() -> str:
    """Get available download formats section"""
    sections = parse_cv_sections()
    formats_section = sections.get("Available Download Formats", "")
    
    if not formats_section:
        return "No download formats found"
    
    return f"## Available Download Formats\n\n{formats_section}"

@mcp.tool()
def get_all_sections() -> str:
    """Get list of all available CV sections"""
    sections = parse_cv_sections()
    
    result = "## Available CV Sections\n\n"
    for i, section_name in enumerate(sections.keys(), 1):
        result += f"{i}. {section_name}\n"
    
    result += "\nUse the specific section tools to get detailed content for each section."
    return result

@mcp.tool()
def get_section_by_name(section_name: str) -> str:
    """Get content of a specific CV section by name"""
    sections = parse_cv_sections()
    
    # Find matching section (case insensitive)
    for section_key in sections.keys():
        if section_name.lower() == section_key.lower():
            return f"## {section_key}\n\n{sections[section_key]}"
    
    # If exact match not found, try partial match
    for section_key in sections.keys():
        if section_name.lower() in section_key.lower():
            return f"## {section_key}\n\n{sections[section_key]}"
    
    available_sections = ", ".join(sections.keys())
    return f"Section '{section_name}' not found. Available sections: {available_sections}"
