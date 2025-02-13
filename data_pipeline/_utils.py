import pandas as pd
from _database import DatabaseTrain, DatabaseItem
from psycopg2.extras import execute_values
import glob

class LoadProcessor:
    def __init__(self):
        self.path = {
            "train" : "./source_files/treino/*.csv",
            "item" : "./source_files/itens/*.csv"
        }

    def process(self, database_cls, path_key):
        with database_cls() as db:
            db.recreate_table()
            self._db_insert_all_csv(db, self.path[path_key])

    def train(self):
        self.process(DatabaseTrain, "train")

    def item(self):
        self.process(DatabaseItem, "item")

    def _db_insert_all_csv(self, database, path):
        for fpath in glob.glob(f"{path}"):
            df = pd.read_csv(fpath, delimiter=",")
            if getattr(database, "columns_explode", False):
                self._df_rule_exclude(df)
            self._db_batch_insert(database, df)

    def _df_rule_exclude(self, df):
        df.drop(columns=['timestampHistory_new'], inplace=True) 

    def _db_insert(self, df, database):
        rows_to_insert = list(df.itertuples(index=False, name=None))
        execute_values(database.cursor, database.insert_table(), rows_to_insert)
        database.conn.commit()

    def _get_num_batches(self, len_df, batch_size):
        return len_df // batch_size + (1 if len_df % batch_size else 0)

    def _db_batch_insert(self, database, df, batch_size=1000):
        num_batches = self._get_num_batches(len(df), batch_size)

        for batch_index in range(num_batches):

            df_batch = self._df_get_batch(batch_index, batch_size, df)
            if getattr(database, "columns_explode", False):
                df_batch = self._df_rule_explode(df_batch, database.columns_explode)
            self._db_insert(df_batch, database)
            print(f"Processed batch {batch_index + 1}/{num_batches}")    

    def _df_get_batch(self, batch_index, batch_size, df):
        start = batch_index * batch_size
        end = (batch_index + 1) * batch_size
        return df.iloc[start:end]

    def _df_rule_explode(self, df, columns_explode):
        df = df.copy()
        df[columns_explode] = df[columns_explode].apply(lambda col: col.fillna('').astype(str).str.split(','))
        return df.explode(columns_explode).reset_index(drop=True)