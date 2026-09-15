import streamlit as st

from app.ui.api_client import (
    ask_dataforge,
    check_health,
    get_catalog,
    get_quality,
)


st.set_page_config(
    page_title="DataForge AI",
    page_icon="🤖",
    layout="wide",
)


# Responsive CSS (kept small and focused)
st.markdown(
    """
    <style>
    .stCodeBlock pre { white-space: pre-wrap; }
    .streamlit-expanderHeader { font-weight: 600; }
    @media (max-width: 600px) {
        .css-1d391kg { padding: 0.5rem 1rem; }
        .stApp { padding: 0.5rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("🤖 DataForge AI")

st.markdown(
    """
    **AI-powered data intelligence platform**

    Ask questions about your business data using natural language.
    """
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("DataForge")

    st.markdown(
        """
        ### Modules

        🧠 AI Query  
        📚 Data Catalog  
        🔍 Data Quality  
        ❤️ System Health
        """
    )

    st.divider()

    if st.button("Check API Health"):

        try:
            health = check_health()
            st.success(health.get("status", "unknown"))
        except Exception as error:
            st.error(f"API unavailable: {error}")


# --------------------------------------------------
# Main tabs
# --------------------------------------------------

tab_query, tab_catalog, tab_quality = st.tabs(
    [
        "🧠 AI Query",
        "📚 Data Catalog",
        "🔍 Data Quality",
    ]
)


# --------------------------------------------------
# AI Query
# --------------------------------------------------

with tab_query:

    st.subheader("Ask DataForge")

    question = st.text_input(
        "Enter your question",
        placeholder=("Show me the top 5 customers by spending"),
    )

    if st.button("Ask DataForge", type="primary"):

        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("DataForge is thinking..."):
                try:
                    result = ask_dataforge(question)

                    if result.get("success"):
                        st.success("Query completed successfully.")

                        response = result.get("response")
                        sql = result.get("sql")

                        # Responsive: answer and SQL side-by-side on wide
                        col1, col2 = st.columns([2, 1], gap="large")

                        with col1:
                            if response:
                                st.subheader("Answer")
                                # Render response depending on its type so the "Answer" shows
                                # user-friendly output: markdown/text, table, or JSON.
                                if isinstance(response, str):
                                    # Render as markdown (works for plain text too)
                                    st.markdown(response)
                                elif isinstance(response, list):
                                    try:
                                        import pandas as pd

                                        df = pd.DataFrame(response)
                                        st.dataframe(df)
                                    except Exception:
                                        st.json(response)
                                elif isinstance(response, dict):
                                    # If dict contains rows/sample, show a table preview
                                    rows = response.get("rows") or response.get("sample")
                                    if isinstance(rows, list) and rows:
                                        try:
                                            import pandas as pd

                                            df = pd.DataFrame(rows)
                                            st.dataframe(df)
                                        except Exception:
                                            st.json(response)
                                    else:
                                        st.json(response)
                                else:
                                    st.write(response)

                        with col2:
                            if sql:
                                with st.expander("Generated SQL", expanded=False):
                                    st.code(sql, language="sql")

                    else:
                        st.error(result.get("error", "Unknown error"))

                except Exception as error:
                    st.error(f"Request failed: {error}")


# --------------------------------------------------
# Data Catalog
# Responsive: list on left, details on right
# --------------------------------------------------

with tab_catalog:

    st.subheader("📚 Data Catalog")

    if st.button("Load Catalog"):
        try:
            result = get_catalog()

            if not result.get("success"):
                st.error("Unable to load catalog.")
            else:
                tables = result.get("tables", [])

                if not tables:
                    st.info("No catalog information available.")
                else:
                    names = [t.get("table", "Unknown") for t in tables]

                    left, right = st.columns([1, 2], gap="large")

                    with left:
                        selected = st.selectbox("Tables", names)
                        st.write(f"{len(names)} tables")

                    with right:
                        table = next((t for t in tables if t.get("table") == selected), tables[0])
                        st.subheader(selected)

                        # If there is a rows/sample key, show a preview table
                        rows = table.get("rows") or table.get("sample") or []
                        if isinstance(rows, list) and rows:
                            try:
                                import pandas as pd

                                df = pd.DataFrame(rows)
                                st.dataframe(df)
                            except Exception:
                                st.json(table)
                        else:
                            st.json(table)

        except Exception as error:
            st.error(f"Catalog request failed: {error}")


# --------------------------------------------------
# Data Quality
# Responsive: KPI summary + expandable details
# --------------------------------------------------

with tab_quality:

    st.subheader("🔍 Data Quality")

    if st.button("Run Quality Check"):
        try:
            result = get_quality()

            if not result.get("success"):
                st.error("Unable to load quality report.")
            else:
                report = result.get("report", {})

                # Show top-level numeric KPIs if present
                left, right = st.columns([1, 2], gap="large")

                with left:
                    # Common fields to promote to metrics
                    metrics = {
                        "tables": report.get("tables_checked") or report.get("table_count") or len(report.get("tables", [])),
                        "anomalies": report.get("anomalies_count") or report.get("issues", 0),
                    }
                    for k, v in metrics.items():
                        try:
                            st.metric(label=k.capitalize(), value=str(v))
                        except Exception:
                            st.write(f"{k}: {v}")

                with right:
                    st.subheader("Report Details")
                    with st.expander("Full JSON report", expanded=False):
                        st.json(report)

        except Exception as error:
            st.error(f"Quality request failed: {error}")
