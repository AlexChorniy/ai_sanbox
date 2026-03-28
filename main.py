import os
from crewai import Agent, Task, Crew, Process, LLM # Use native LLM
from crewai_tools import FileWriterTool

# 1. Initialize Gemini using the native CrewAI LLM class
# The model string MUST start with 'gemini/' for the provider to be recognized
gemini_llm = LLM(
    # Option A: The reliable workhorse
    model="google/gemini-2.5-flash", 
    
    # Option B: If you want to use the newest one from your list:
    # model="google/gemini-3.1-flash-lite-preview",
    
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

# 2. Setup the Project Workspace tool
file_writer = FileWriterTool(directory="/projects")

# 3. Define the AI Factory Team
architect = Agent(
    role='Lead Systems Architect',
    goal='Plan a modular project structure for: {user_request}',
    backstory='Expert in clean architecture. You output file maps.',
    llm=gemini_llm,
    verbose=True
)

developer = Agent(
    role='Senior Full-Stack Engineer',
    goal='Write implementation code for planned files.',
    backstory='You write optimized code. You do NOT save files.',
    llm=gemini_llm,
    verbose=True
)

reviewer = Agent(
    role='Security Officer',
    goal='Verify code and save files to /projects using FileWriterTool.',
    backstory='You are the only one allowed to write to the disk.',
    tools=[file_writer],
    llm=gemini_llm,
    verbose=True
)

# 4. Define the Workflow
plan_task = Task(
    description="Analyze request: {user_request}. List files/folders.",
    expected_output="A structured file map.",
    agent=architect
)

dev_task = Task(
    description="Write code for every file. Output raw code blocks.",
    expected_output="Full source code.",
    agent=developer,
    context=[plan_task]
)

review_task = Task(
    description="Review code and use FileWriterTool to save each file.",
    expected_output="Confirmation of build.",
    agent=reviewer,
    context=[dev_task]
)

# 5. Form the Crew
factory_crew = Crew(
    agents=[architect, developer, reviewer],
    tasks=[plan_task, dev_task, review_task],
    process=Process.sequential
)

if __name__ == "__main__":
    request = "A simple Python script that scrapes a quote website."
    print(f"### Launching AI Factory for: {request} ###")
    factory_crew.kickoff(inputs={'user_request': request})