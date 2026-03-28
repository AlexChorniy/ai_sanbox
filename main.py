import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileWriterTool
from dotenv import load_dotenv

load_dotenv()

# --- 1. LLM CONFIGURATION (AI PLUS HYBRID) ---

# Gemini 3.1 Pro: High reasoning for Architecture and Review
gemini_pro = LLM(
    model="google/gemini-3.1-pro-preview",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

# Gemini 3.1 Flash: Fast generation for bulk coding
gemini_flash = LLM(
    model="google/gemini-3.1-flash-lite-preview",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# --- 2. TOOLS SETUP ---
# This tool allows the Reviewer to save the final files to the disk
file_writer = FileWriterTool(directory="/projects")

# --- 3. AGENT DEFINITIONS ---
architect = Agent(
    role='Lead Systems Architect',
    goal='Design a modular, scalable structure for: {user_request}',
    backstory='Expert in SOLID principles and clean architecture. You define the file map.',
    llm=gemini_pro,
    verbose=True
)

developer = Agent(
    role='Senior Software Engineer',
    goal='Write the full implementation code for the planned files.',
    backstory='You write optimized, clean Python code. You output raw code blocks only.',
    llm=gemini_flash,
    verbose=True
)

reviewer = Agent(
    role='Security & Quality Lead',
    goal='Review the code for bugs/vulnerabilities and save them to /projects.',
    backstory='You verify logic and use the FileWriterTool to finalize the build.',
    tools=[file_writer],
    llm=gemini_pro,
    verbose=True
)

# --- 4. TASK DEFINITIONS ---
plan_task = Task(
    description="Analyze the request: {user_request}. Output a list of required files and folders.",
    expected_output="A structured directory tree and descriptions of each file's purpose.",
    agent=architect
)

dev_task = Task(
    description="Based on the architect's plan, write the full source code for every file.",
    expected_output="The complete source code for all planned files, formatted as markdown code blocks.",
    agent=developer,
    context=[plan_task]
)

review_task = Task(
    description="Review the developer's code. If it is correct, use the FileWriterTool to save each file to /projects.",
    expected_output="Confirmation that all files have been reviewed and successfully saved.",
    agent=reviewer,
    context=[dev_task]
)

# --- 5. CREW ASSEMBLY ---
factory_crew = Crew(
    agents=[architect, developer, reviewer],
    tasks=[plan_task, dev_task, review_task],
    process=Process.sequential,
    memory=True # AI Plus allows for more complex memory handling
)

if __name__ == "__main__":
    user_input = "A Flask API with JWT authentication and a SQLite database."
    print(f"\n🚀 Launching AI Factory for: {user_input}\n")
    
    result = factory_crew.kickoff(inputs={'user_request': user_input})
    
    print("\n\n########################")
    print("## FACTORY RUN COMPLETE ##")
    print("########################\n")
    print(result)