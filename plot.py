from utils.call_models import get_embedding_model, get_gen_model
from utils.call_prompt import PROMPT    
from utils.config import CONFIG

import re
import pandas as pd
import plotly.express as px

EMBEDDING_MODEL = CONFIG["EMBEDDING_MODEL"]
LLM_MODEL = CONFIG["LLM_MODEL"]

CHUNK_SIZE = CONFIG["CHUNK_SIZE"]
CHUNK_OVERLAP = CONFIG["CHUNK_OVERLAP"]
TOP_K = CONFIG["TOP_K"]

QUERY = CONFIG["QUERY"]

from langchain_community.document_loaders.csv_loader import CSVLoader


import re
import pandas as pd
import plotly.express as px

def extract_code(llm_response: str):
    """Extracts code blocks (SQL or Pandas) from LLM response."""
    # Look for ```sql ... ``` or ```python ... ```
    match = re.search(r"```(.*?)```", llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return llm_response  # fallback

def execute_and_plot(code: str, df: pd.DataFrame):
    """
    Executes generated Pandas/SQL code and plots using Plotly.
    For SQL: Use duckdb or sqlite.
    For Pandas: Directly exec code.
    """
    if "select" in code.lower():
        # SQL mode
        import duckdb
        result_df = duckdb.query(code).to_df()
    else:
        # Pandas mode
        local_vars = {"df": df, "pd": pd}
        exec(code, {}, local_vars)
        result_df = local_vars.get("result_df", None)

    if result_df is None or result_df.empty:
        print("No result returned.")
        return None

    # Auto-plot based on KB rules (example mapping)
    if result_df.shape[1] == 2:
        fig = px.line(result_df, x=result_df.columns[0], y=result_df.columns[1])
    elif result_df.shape[1] == 3:
        fig = px.bar(result_df, x=result_df.columns[0], y=result_df.columns[1], color=result_df.columns[2])
    else:
        fig = px.scatter(result_df, x=result_df.columns[0], y=result_df.columns[1])

    fig.show()
    return result_df
