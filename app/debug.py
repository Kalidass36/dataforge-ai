from app.debugger.debugger import PipelineDebugger


def main():

    debugger = PipelineDebugger()

    print("=" * 60)
    print("DATAFORGE AI PIPELINE DEBUGGER")
    print("=" * 60)

    print("Type 'exit' to quit.")

    while True:

        error_message = input(
            "\nPaste pipeline/database error: "
        )

        if error_message.lower().strip() == "exit":
            break

        result = debugger.debug(
            error_message
        )

        print("\nERROR TYPE:")
        print(result["error_type"])

        print("\nLIKELY ROOT CAUSE:")
        print(result["root_cause"])

        print("\nAI RECOMMENDATION:")
        print(result["recommendation"])


if __name__ == "__main__":
    main()