import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileWriterTool
from dotenv import load_dotenv

load_dotenv()

# --- 1. LLM CONFIGURATION ---
gemini_pro = LLM(
    model="google/gemini-3.1-pro-preview",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

gemini_flash = LLM(
    model="google/gemini-3.1-flash-lite-preview",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# --- 2. TOOLS SETUP ---
# Ensure this matches your docker-compose volume (usually /project3)
file_writer = FileWriterTool(directory="/project3")

# --- 3. AGENT DEFINITIONS ---
architect = Agent(
    role='Lead Mobile Architect',
    goal='Design a 2026-standard React Native structure for: {user_request}',
    backstory='Expert in Expo Router, New Architecture, and performance optimization.',
    llm=gemini_pro,
    verbose=True
)

developer = Agent(
    role='Senior Mobile Engineer',
    goal='Write implementation code in TypeScript for React Native (Expo).',
    backstory='Expert in React Native and NativeWind. You write clean TSX code.',
    llm=gemini_flash,
    max_iter=5,
    max_execution_time=120, 
    verbose=True
)

reviewer = Agent(
    role='System Integrity & Quality Lead',
    goal='Validate 2026 Node/Expo compatibility and save verified files to /project3',
    backstory=(
        "You are an expert at Catching Node.js 'Package Export' errors. "
        "You are an expert at Mac-based development environments."
        "You ensure projects include specific troubleshooting for 'EMFILE' "
        "errors and Node 20+ export mapping."
        "You must ensure that the package.json uses @expo/metro-config v0.17+ "
        "to remain compatible with Node 20+. You do not save files unless "
        "the versions are perfectly aligned for a clean 'npx expo start'."
    ),
    tools=[file_writer],
    llm=gemini_pro,
    verbose=True,
)

# --- 4. TASK DEFINITIONS ---

# 1. Architecture Task (Defining the package.json)
mobile_plan_task = Task(
    description=(
        "Design a React Native TODO app using the 2026 'New Architecture'. "
        "Include a detailed 'package.json' content with Expo SDK 54, "
        "Zustand, and MMKV. Define the full folder structure (app/, src/components/, src/store/)."
    ),
    expected_output="A full file map and the exact string content for package.json.",
    agent=architect
)

# 2. Coding Task
mobile_dev_task = Task(
    description=(
        "Write the TypeScript code for the TODO app based on the architect's plan. "
        "Ensure all imports match the suggested folder structure."
    ),
    expected_output="Complete source code for all .tsx and .ts files.",
    agent=developer,
    context=[mobile_plan_task]
)

# 3. Review & File Creation Task (The "Execution" Step)
mobile_review_task = Task(
    description=(
        "1. MANDATORY CHECK: Ensure 'package.json' includes @expo/metro-config@^0.17.0 "
        "and metro-cache@^0.80.0 to prevent ERR_PACKAGE_PATH_NOT_EXPORTED.\n"
        "2. MANDATORY CHECK: Verify the 'setup_mobile.sh' script includes a version "
        "check for Node.js >= 20.\n"
        "3. Review the TSX code for performance bottlenecks.\n"
        "4. Use FileWriterTool to save all files ONLY after these checks pass."
        "5. MANDATORY: Verify package versions align with Expo SDK 51 standards.\n"
        "6. MANDATORY: Update 'setup_mobile.sh' to include 'brew install watchman' "
        "and 'ulimit -n 10000' to prevent EMFILE errors on Mac.\n"
        "3. Save all files to /project3."
    ),
    expected_output="A verified, bootable React Native project folder in /project3. A verified project folder with Mac-optimized setup scripts.",
    agent=reviewer,
    context=[mobile_dev_task]
)

# --- 5. CREW ASSEMBLY ---
mobile_crew = Crew(
    agents=[architect, developer, reviewer],
    tasks=[mobile_plan_task, mobile_dev_task, mobile_review_task],
    process=Process.sequential,
    memory=True,
    memory_config={
        "llm": gemini_pro,  # Tells Memory to use Gemini Pro for thinking
        "embedder": {
            "provider": "google",
            "config": {
                "model": "models/gemini-embedding-2-preview", # Use the 2026 Google embedder from your list
                "task_type": "retrieval_document",
                "title": "Memory Embedding"
            }
        }
    }
)

if __name__ == "__main__":
    result = mobile_crew.kickoff(inputs={
        'user_request': 'A modern TODO app with local persistence and native haptics.'
    })
    
    print(f"Total Tokens Used: {result.token_usage}")
    print("\n\n########################")
    print("## FACTORY RUN COMPLETE ##")
    print("########################\n")
    print(result)