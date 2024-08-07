# 🏢 Multi-AI Agent Content Creation Platform 🏢

## What is this project?

This project is a sophisticated AI-powered content creation system that leverages multiple AI agents to research and write diverse, high-quality content on any given topic. It's designed to be flexible, customizable, and easily configurable through a simple JSON file.

## Key Features

- **Multi-Agent Workflow:** Utilizes a team of AI agents including a researcher and multiple writers.
- **Customizable Prompts:** Easily adjust agent behaviors and output styles through configuration.
- **Streamlit Interface:** User-friendly web interface for running and monitoring the workflow.
- **Flexible Output:** Generate various content types, from blog posts to in-depth reports.

## How It Works

1. **Research Phase:** The researcher agent gathers and analyzes information on the specified topic.
2. **Writing Phase:** Multiple writer agents create diverse content based on the research.
3. **Synthesis:** A final step combines and refines the generated content.

## Technical Details

- **Language:** Python 3.7+
- **AI Framework:** Google's Gemini API
- **Web Interface:** Streamlit
- **Configuration:** JSON-based
- **Key Libraries:** 
  - `griptape`: For creating and managing AI agents
  - `google-generativeai`: Interface with Gemini AI models
  - `streamlit`: Web app framework