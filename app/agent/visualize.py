from app.agent.graph import (
    build_graph,
)


def main():

    graph = build_graph()

    print(
        graph.get_graph().draw_mermaid()
    )


if __name__ == "__main__":

    main()