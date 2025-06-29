# AgentTaskPlanner
class AgentTaskPlanner:
    @staticmethod
    def plan(task_input: str) -> list:
        if "analyze" in task_input:
            return ["summarize text", "extract key metrics", "generate insights"]
        return [task_input]
