import asyncio
from mcp.server.fastmcp import FastMCP
from src.dialog import show_feedback_dialog

mcp = FastMCP("mcp-feedback-lite")


@mcp.tool()
async def interactive_feedback(
    project_directory: str = ".",
    summary: str = "已完成您请求的任务。",
    timeout: int = 600,
) -> str:
    """Interactive feedback collection tool for LLM agents.

    USAGE RULES:
    1. After completing any task or subtask, call this tool to get user feedback.
    2. Unless receiving termination instructions, repeatedly call this tool.
    3. When user feedback is not empty, adjust behavior based on feedback and call again.
    4. Only stop when user submits empty content or says exit/quit/done/退出/结束/完成.
    5. Summarize what you have done in the summary parameter.

    Args:
        project_directory: Project directory path for context
        summary: Summary of AI work completed for user review
        timeout: Timeout in seconds for waiting user feedback (default: 600)

    Returns:
        User feedback text. Empty string means user wants to end the session.
    """
    loop = asyncio.get_running_loop()
    feedback = await loop.run_in_executor(
        None, show_feedback_dialog, summary, project_directory, timeout
    )
    return feedback or ""


def main():
    mcp.run()
