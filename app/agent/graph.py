from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.agent.state import (
    DataForgeState,
)

from app.agent.nodes import (
    router_node,
    catalog_node,
    quality_node,
    sql_node,
    response_node,
)


def route_after_router(state):

    intent = state.get(
        "intent"
    )

    if intent == "catalog":

        return "catalog"

    if intent == "quality":

        return "quality"

    return "sql"


def build_graph():

    graph = StateGraph(
        DataForgeState
    )

    graph.add_node(
        "router",
        router_node
    )

    graph.add_node(
        "catalog",
        catalog_node
    )

    graph.add_node(
        "quality",
        quality_node
    )

    graph.add_node(
        "sql",
        sql_node
    )

    graph.add_node(
        "response",
        response_node
    )

    graph.add_edge(
        START,
        "router"
    )

    graph.add_conditional_edges(
        "router",
        route_after_router,
        {
            "catalog": "catalog",
            "quality": "quality",
            "sql": "sql",
        }
    )

    graph.add_edge(
        "catalog",
        "response"
    )

    graph.add_edge(
        "quality",
        "response"
    )

    graph.add_edge(
        "sql",
        "response"
    )

    graph.add_edge(
        "response",
        END
    )

    return graph.compile()