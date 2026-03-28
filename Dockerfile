FROM python:3.12-slim

# Install system dependencies for git and networking
RUN apt-get update && apt-get install -y \
    curl git && \
    rm -rf /var/lib/apt/lists/*

# Install CrewAI with the native Google GenAI provider
RUN pip install --no-cache-dir \
    "crewai[google-genai]" \
    crewai-tools \
    python-dotenv

WORKDIR /app

# Ensure the output directory exists
RUN mkdir -p /projects

COPY main.py /app/main.py

CMD ["python", "main.py"]