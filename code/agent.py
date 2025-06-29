# agent.py — orchestrator integrating all core Amplifai agents

from .planner.AgentTaskPlanner import AgentTaskPlanner
from .prompt.PromptCraft import PromptCraft
from .tool.ToolCaller import ToolCaller
from .audit.QuarantineEngine import QuarantineEngine
from .sync.ContentBlockSync import ContentBlockSync
from .core.ImmutableCore import ImmutableCore
from .core.SelfModEngine import SelfModEngine
from .core.ExtractorEngine import ExtractorEngine
from .runtime.AMPNode import AMPNode
from .finance.IncomeAgent import IncomeAgent
from .security.TrustStack import TrustStack
from .ui.UIIntentEngine import UIIntentEngine
from .schema import AgentTask, AgentResponse
from .logger import get_logger

logger = get_logger(__name__)

def execute_task(task: AgentTask) -> AgentResponse:
    logger.info(f"Planning task: {task.task_id}")
    subtasks = AgentTaskPlanner.plan(task.input)
    full_output = []

    for sub in subtasks:
        prompt = PromptCraft.build(sub)
        tool_output = ToolCaller.call(["search", "summarize"], sub)

        if not QuarantineEngine.verify(tool_output):
            tool_output = SelfModEngine.evolve(tool_output)
            fragments = ExtractorEngine.salvage(tool_output)
            tool_output += "\nRecovered Logic:\n" + "\n".join(fragments)

        if task.input.lower().startswith("income"):
            income_steps = IncomeAgent.generate_plan({})
            tool_output += "\nIncome Plan:\n" + "\n".join(income_steps)

        if not ImmutableCore.validate_and_commit(tool_output):
            tool_output = "[BLOCKED BY IMMUTABLE CORE]"

        amp_exec = AMPNode.run(sub)
        display_text = UIIntentEngine.morph_response(tool_output + "\n" + amp_exec)

        full_output.append(f"[{sub}]\nPrompt:\n{prompt}\n{display_text}\n")

    result = "\n---\n".join(full_output)
    ContentBlockSync.update(task.task_id, result)
    return AgentResponse(task_id=task.task_id, content=result)
