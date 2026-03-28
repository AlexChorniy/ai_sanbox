import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import tool

# --- STEP 1: Define the "Hands" (The File Tool) ---
class FileTools:
    @tool("write_file")
    def write_file(content: str, filename: str):
        """Writes content to a specific file within the /projects directory."""
        # Enforce the Docker sandbox path
        base_path = "/projects"
        filepath = os.path.join(base_path, filename)
        
        try:
            # Ensure subdirectories exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w") as f:
                f.write(content)
            return f"Successfully wrote to {filename}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

# --- STEP 2: Define the "Minds" (The Agents) ---
architect = Agent(
    role='System Architect',
    goal='Plan the file structure for: {user_request}',
    backstory="You are a senior architect. You output only a list of filenames and their purpose.",
    allow_delegation=False,
    verbose=True
)

developer = Agent(
    role='Senior Developer',
    goal='Write clean, documented code and save it using the write_file tool',
    backstory="You take the Architect's plan and turn it into actual files in the /projects folder.",
    tools=[FileTools.write_file],
    verbose=True
)

# --- STEP 3: Define the "Mission" (The Tasks) ---
plan_task = Task(
    description="Analyze the request: {user_request}. Create a list of files needed.",
    expected_output="A structured list of all files for the project.",
    agent=architect
)

write_task = Task(
    description="Take the architecture plan and write the actual code for each file to the /projects directory.",
    expected_output="Confirmation that all files have been written to disk.",
    agent=developer,
    context=[plan_task]
)

# --- STEP 4: Fire up the Factory ---
my_crew = Crew(
    agents=[architect, developer],
    tasks=[plan_task, write_task],
    process=Process.sequential
)

if __name__ == "__main__":
    print("### AI-First Factory Started ###")
    user_input = "A simple Flask API with a single 'hello' endpoint and a Dockerfile"
    my_crew.kickoff(inputs={'user_request': user_input})