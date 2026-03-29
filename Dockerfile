FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl git nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Install CrewAI and tools
RUN pip install --no-cache-dir \
    "crewai[google-genai]" \
    crewai-tools \
    python-dotenv

WORKDIR /app

# Create projects directory
RUN mkdir -p /project3

# Copy the main script
COPY main.py /app/main.py

# CRITICAL: This ensures that any script created in /projects 
# can be modified/executed by the container user
RUN chmod -R 777 /project3

CMD ["python", "main.py"]