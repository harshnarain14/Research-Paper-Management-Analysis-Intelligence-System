# This file decides when to call which MCP-style tool
# based on the user query and combines tool output with LLM responses

from mcp.tools import (
    paper_metadata_lookup_tool,
    related_work_discovery_tool,
    trend_analytics_tool
)


def route_tools(query: str, paper, embedded_chunks: list) -> dict:
    """
    This function decides which MCP tool to call
    based on the user's query.

    This is a simple rule-based router to keep logic explainable.
    """

    query_lower = query.lower()

    # Case 1: Metadata-related questions
    if "year" in query_lower or "published" in query_lower or "citation" in query_lower:
        metadata = paper_metadata_lookup_tool(paper.title)
        return {
            "tool_used": "paper_metadata_lookup",
            "data": metadata
        }

    # Case 2: Related work questions
    if "related" in query_lower or "similar" in query_lower:
        related_work = related_work_discovery_tool(
            paper.paper_id,
            embedded_chunks
        )
        return {
            "tool_used": "related_work_discovery",
            "data": related_work
        }

    # Case 3: Trend / growth questions
    if "trend" in query_lower or "growth" in query_lower or "emerging" in query_lower:
        trend_data = trend_analytics_tool(query)
        return {
            "tool_used": "trend_analytics",
            "data": trend_data
        }

    # Default: No tool required
    return {
        "tool_used": None,
        "data": None
    }
