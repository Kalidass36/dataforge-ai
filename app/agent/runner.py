from app.agent.graph import (
    build_graph,
)


def main():

    graph = build_graph()

    print("=" * 60)
    print("DATAFORGE LANGGRAPH AGENT")
    print("=" * 60)

    print(
        "\nType 'exit' to quit."
    )

    while True:

        question = input(
            "\nAsk DataForge: "
        )

        if question.lower().strip() == "exit":

            break

        state = {
            "user_input": question,
            "retry_count": 0,
        }

        try:

            result = graph.invoke(
                state
            )

            print(
                "\nIntent:"
            )

            print(
                result.get(
                    "intent"
                )
            )

            print(
                "\nResponse:"
            )

            print(
                result.get(
                    "response"
                )
            )

            if result.get("sql"):

                print(
                    "\nSQL:"
                )

                print(
                    result["sql"]
                )

        except Exception as error:

            print(
                "\nDataForge Error:"
            )

            print(error)


if __name__ == "__main__":

    main()