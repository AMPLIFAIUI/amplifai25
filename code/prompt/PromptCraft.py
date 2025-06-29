# PromptCraft
class PromptCraft:
    @staticmethod
    def build(task_input: str) -> str:
        return f"""You are an advanced reasoning agent.

Task:
{task_input}

Use tools if needed. Always explain your steps before final answer."""
