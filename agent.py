import os
from interpreter import interpreter
from dashscope import Generation

# Load environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\Users\User\Desktop\OpenAgent_Recovered\.env")

# Set project root
PROJECT_ROOT = os.getenv("PROJECT_ROOT")
os.chdir(PROJECT_ROOT)

# Initialize Qwen via DashScope API
Generation.api_key = os.getenv("DASHSCOPE_API_KEY")

def qwen_plan(task):
    """Ask Qwen to generate code to complete a task"""
    prompt = f"""
You are an autonomous agent controller.
I will give you tasks, and you must write Python/bash/code to complete them.
Always return full executable code blocks.

Task: {task}
"""

    print("\n🧠 Sending task to Qwen...")
    response = Generation.call(model="qwen-turbo", prompt=prompt)
    
    if not hasattr(response, "output") or not hasattr(response.output, "text"):
        print("❌ Failed to get valid plan from Qwen")
        print("Raw Response:", response)
        return ""

    plan = response.output.text.strip()
    print("\n📝 Generated Code Plan:")
    print(plan)
    return plan


def run_agent_task(task):
    """Run a task using Qwen as planner + Open Interpreter as executor"""
    print(f"\n🧠 Agent Task: {task}")
    code_plan = qwen_plan(task)

    if not code_plan:
        print("🚫 No valid code plan received.")
        return

    print("\n⚙️ Running in Open Interpreter...")
    interpreter.chat(code_plan)


# Example Task
run_agent_task("List all JavaScript files in the current directory and count how many functions each has")