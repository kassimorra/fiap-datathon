import psycopg2
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#nltk.download('stopwords')

def get_data_db(sql_query: str):
    conn_params: dict[str, str] = {
        "dbname":"globo",
        "user":"postgres",
        "password":"admin1234",
        "host":"localhost",
        "port":"5432"
    }

    with psycopg2.connect(**conn_params) as conn:
        return pd.read_sql(sql_query, conn)
   
def get_user_history(user_id: str) -> pd.DataFrame:
    columns: str = 'history, timestamphistory, news_concat'
    sql_query: str = f"select {columns} from table_full where userid = '{user_id}' order by scrollpercentagehistory desc limit 5"
    user_data = get_data_db(sql_query)
    user_data['read'] = True
    return user_data

def get_last_news_date() -> str:
    sql_query: str = "select max(modified) as modified from table_item"
    return get_data_db(sql_query)

def get_last_news(days: int) -> pd.DataFrame:
    last_date: str = get_last_news_date()['modified'].iloc[0]
    columns: str = 'history, modified, page_url, news_concat'
    sql_query: str = f"select {columns} from table_item where modified >= '{last_date}'::timestamp - INTERVAL '{days} days' order by modified desc"
    last_news = get_data_db(sql_query)
    last_news['read'] = False
    return last_news

def remove_read_news(last_news, user_data) -> pd.DataFrame:
    remove_read_news = last_news[~last_news['history'].isin(user_data['history'])]
    return remove_read_news

def get_prediction(predict_data, history) -> pd.DataFrame:
    portuguese_stop_words = stopwords.words('portuguese')
    tfidf: TfidfVectorizer = TfidfVectorizer(stop_words=portuguese_stop_words)
    tfidf_matrix = tfidf.fit_transform(predict_data['news_concat'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    idx: list[int] = predict_data.index[predict_data['history'].isin(history)].tolist()
    sim_matrix = cosine_sim[idx]
    aggregated_scores = sim_matrix.sum(axis=0)
    sim_scores = list(enumerate(aggregated_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:8]
    news_indices = [i[0] for i in sim_scores]
    df_output: pd.DataFrame = predict_data.iloc[news_indices][predict_data.iloc[news_indices]['read'] == False]
    return df_output
