# Use the 2026 standard slim image
FROM python:3.12-slim

# Install system dependencies for MCP and coding
RUN apt-get update && apt-get install -y \
    curl git nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Install the MCP Filesystem server (the "hands" of the AI)
RUN npm install -g @modelcontextprotocol/server-filesystem

# Install your Agent Framework
RUN pip install crewai langchain-openai

WORKDIR /app
COPY . /app

# The AI will work inside the /projects directory
RUN mkdir /projects

CMD ["python", "main.py"]