from code.agent import execute_task
from code.schema import AgentTask

task = AgentTask(task_id="test-001", input="generate passive income ideas")
response = execute_task(task)
print(response.content)
