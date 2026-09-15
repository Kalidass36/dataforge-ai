def classify_intent(user_input):

    text = user_input.lower()

    quality_keywords = [
        "quality",
        "null",
        "missing",
        "duplicate",
        "anomaly",
        "data issue",
        "data problem",
    ]

    catalog_keywords = [
        "schema",
        "table",
        "column",
        "relationship",
        "catalog",
        "metadata",
        "describe",
    ]

    for keyword in quality_keywords:

        if keyword in text:

            return "quality"

    for keyword in catalog_keywords:

        if keyword in text:

            return "catalog"

    return "sql"