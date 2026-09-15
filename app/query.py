from app.sql.nl_to_sql import NaturalLanguageSQL


def _print_debug_info(debug: dict):

    print("\nDEBUGGER")
    print("-" * 50)
    print("Error Type:", debug["error_type"])
    print("\nRoot Cause:", debug["root_cause"])
    print("\nAI Recommendation:")
    print(debug["recommendation"])


def _print_response(response: dict):

    print("\nGenerated / Corrected SQL:")
    print("-" * 50)
    print(response["sql"])

    if response["success"]:
        print("\nResults:")
        print("-" * 50)

        rows = response["result"]["rows"]

        if not rows:
            print("No results found.")
        else:
            for row in rows:
                print(row)

        return

    print("\nERROR:")
    print(response["error"])

    if "debug" in response:
        _print_debug_info(response["debug"])


def main():

    system = NaturalLanguageSQL()

    print("=" * 50)
    print("DataForge Natural Language → SQL")
    print("=" * 50)
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk DataForge: ")

        if question.lower().strip() == "exit":
            break

        response = system.ask(question)
        _print_response(response)


if __name__ == "__main__":
    main()