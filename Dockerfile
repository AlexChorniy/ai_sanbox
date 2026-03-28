FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl git && \
    rm -rf /var/lib/apt/lists/*

# The key change: adding [google-genai] to the crewai install
RUN pip install --no-cache-dir \
    "crewai[google-genai]" \
    crewai-tools \
    python-dotenv

WORKDIR /app
COPY main.py /app/main.py

RUN mkdir -p /projects

CMD ["python", "main.py"]