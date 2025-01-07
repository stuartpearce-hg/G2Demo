import os
from crewai import Agent, Task, Crew
# Importing crewAI tools
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    PDFSearchTool
)

# Set up API keys
os.environ["AZURE_ENDPOINT"]="https://hggpt4.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "60a346a5bd014405b93a75c287160105"
os.environ["OPENAI_API_DEPLOYMENT_NAME"]="gpt-4o"
os.environ["OPENAI_API_TYPE"]="azure"
os.environ["OPENAI_API_VERSION"]="2023-09-01-preview"

# Instantiate tools
docs_tool = DirectoryReadTool(directory='/inputs')
file_tool = FileReadTool()
pdf_tool = PDFSearchTool()

# Create agents
researcher = Agent(
    role='Client Document Analyst',
    goal='Extract key data points from investor subscription documents',
    backstory='An expert analyst with a keen eye for detail.',
    tools=[docs_tool, file_tool, pdf_tool],
    verbose=True
)

writer = Agent(
    role='Report Writer',
    goal='Write concise and accurate reports of data from subscription documents',
    backstory='A skilled writer with a passion for technology.',
    tools=[docs_tool, file_tool],
    verbose=True
)

# Define tasks
data_extract = Task(
    description='Review the client subscription documents and provide a list of client names.',
    expected_output='A list of clients and the funds they are subscribed to.',
    agent=researcher
)

write = Task(
    description='Write an concise review of the funds each client subscribes to.',
    expected_output='A list of clients and the funds they are subscribed to.',
    agent=writer,
    output_file='outputs/report.md'  # The final report will be saved here
)

# Assemble a crew with planning enabled
crew = Crew(
    agents=[researcher, writer],
    tasks=[data_extract, write],
    verbose=True,
    planning=True,  # Enable planning feature
)

# Execute tasks
crew.kickoff()
