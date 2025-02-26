from _feast_materialize import FeatureStore
from datetime import datetime
import pandas as pd
import psycopg

def get_data_db(sql_query: str):
    conn_params: dict[str, str] = {
        "dbname":"globo",
        "user":"postgres",
        "password":"admin1234",
        "host":"host.docker.internal",
        # "host":"localhost",
        "port":"5432"
    }

    with psycopg.connect(**conn_params) as conn:
        return pd.read_sql(sql_query, conn)
    
def get_user_history(userid: str) -> pd.DataFrame:
    columns: str = 'userid, timestamphistory as event_timestamp'
    sql_query: str = f"select {columns} from table_full where userid = '{userid}' order by timestamphistory desc limit 15"
    user_data = get_data_db(sql_query)
    return user_data

#entity_df = get_user_history('e7a6c843011a4823501fe0b297c0956d84db3d0f7399f4736336b6807d6a7339')

def get_user_features(userid: str) -> dict:
    store = FeatureStore(repo_path=".")
    feature_refs = [
        "globo_fv:timestamphistory",
        "globo_fv:history",
        "globo_fv:news_concat",
    ]
    # Fetch online features
    historical_features = store.get_historical_features(
        entity_df=get_user_history(userid),
        features=feature_refs,
    )
    # Convert to a DataFrame for easier handling
    features_df = historical_features.to_df()
    return features_df.to_dict(orient="records")