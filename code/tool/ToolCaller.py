# ToolCaller
class ToolCaller:
    @staticmethod
    def call(tools: list, task_input: str) -> str:
        log = []
        for tool in tools:
            log.append(f"Tool `{tool}` used on: {task_input}")
        return "\n".join(log)
