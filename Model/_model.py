import pandas as pd
from _utils import get_user_history, get_last_news, get_prediction_df, remove_read_news

# e7a6c843011a4823501fe0b297c0956d84db3d0f7399f4736336b6807d6a7339

def get_prediction(userid: str) -> dict:
    user_data = get_user_history(userid)
    last_news = get_last_news(10)
    read_news = remove_read_news(last_news, user_data)
    predict_data = pd.concat([user_data, read_news], axis=0, ignore_index=True)
    history: list[str] = ('7fe849c0-4a55-429d-b480-11ee216909dd', '13f2cc37-f575-44d5-b33f-045d0b0a912b')
    df_predict: pd.DataFrame = get_prediction_df(predict_data, history)
    return df_predict.to_dict(orient="records")