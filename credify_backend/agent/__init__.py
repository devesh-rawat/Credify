"""
Agent module for Credify Backend
Using Google Gemini API
"""

# Use Gemini agent as default
from agent.credify_agent import CredifyAgent, get_agent, run_agent_task
from agent.credify_chat_agent import CredifyChatAgent, get_chat_agent, chat_query
from agent.agent_tools import ALL_TOOLS, get_tool_schemas, execute_tool
from agent.agent_tasks import TaskType, get_task_definition, validate_task_params
from agent.agent_runtime import get_metrics, log_agent_activity

__all__ = [
    "CredifyAgent",
    "get_agent",
    "run_agent_task",
    "get_agent",
    "run_agent_task",
    "CredifyChatAgent",
    "get_chat_agent",
    "chat_query",
    "ALL_TOOLS",
    "get_tool_schemas",
    "execute_tool",
    "TaskType",
    "get_task_definition",
    "validate_task_params",
    "get_metrics",
    "log_agent_activity",
]
