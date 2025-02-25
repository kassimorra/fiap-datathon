import pandas as pd
import glob
from ._database import DatabaseTrain, DatabaseItem
from psycopg2.extras import execute_values
from ._correct_itens import CorrectItem

class ProcessParam:
    def __init__(self):
        self.path : dict = {
            "train" : "./source_files/treino/*.csv",
            "item" : "./source_files/itens/*.csv",
            "item_correct" : "./source_files/correct_itens/*.csv"
        }
        self.batch_size : int = 1000
        self._num_batches: int = 0

    @property
    def num_batches(self) -> int:
        return self._num_batches

    @num_batches.setter
    def num_batches(self, new_value: int) -> None:
        self._num_batches = new_value

    def calculate_num_batches(self, len_df: int) -> None:
        self.num_batches = len_df // self.batch_size + (1 if len_df % self.batch_size else 0)

def process_insert_db(df: pd.DataFrame, db: DatabaseTrain, num_batches: int, batch_index: int, fpath: str) -> None:
    rows_to_insert: list = list(df.itertuples(index=False, name=None))
    execute_values(db.cursor, db.insert_table(), rows_to_insert)
    db.conn.commit()
    print(f"dfSize = {len(df)} -> File: {fpath} -> Processed batch: {batch_index + 1}/{num_batches}")

def process_get_df_batch(df: pd.DataFrame, batch_size: int, batch_index: int) -> pd.DataFrame:
    start = batch_index * batch_size
    end = (batch_index + 1) * batch_size
    return df.iloc[start:end]

class Process:
    def __init__(self):
        self._param: ProcessParam = ProcessParam()
        self._database = None
        self._type: str = ''

    def _process_df_rule(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def _setup_database(self) -> None:
        self._database.recreate_table()

    def _process_file(self, fpath: str) -> None:
        df: pd.DataFrame = pd.read_csv(fpath, sep=",", quotechar='"', encoding="utf-8", engine="python", on_bad_lines="skip")
        self._param.calculate_num_batches(len(df))

        for batch_index in range(self._param.num_batches):
            df_batch = process_get_df_batch(df, self._param.batch_size, batch_index)
            df_rule = self._process_df_rule(df_batch)
            process_insert_db(df_rule, self._database, self._param.num_batches, batch_index, fpath)

    def run(self) -> None:
        self._setup_database()
        for fpath in glob.glob(f"{self._param.path[self._type]}"):
            self._process_file(fpath)
        self._database.close()

class ProcessTrain(Process):
    def __init__(self):
        super().__init__()
        self._database: DatabaseTrain = DatabaseTrain()
        self._type: str = 'train'

    def _process_df_rule(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # df.drop(columns=['timestampHistory_new'], inplace=True)
        df[self._database.columns_explode] = df[self._database.columns_explode].apply(lambda col: col.fillna('').astype(str).str.split(','))
        df = df.explode(self._database.columns_explode).reset_index(drop=True)
        df["timestampHistory"] = pd.to_datetime(pd.to_numeric(df["timestampHistory"]), unit="ms")
        df["timestampHistory_new"] = pd.to_datetime(pd.to_numeric(df["timestampHistory_new"]), unit="ms")
        df["history"] = df["history"].str.replace(' ', '', regex=False)
        return df

class ProcessItem(Process):
    def __init__(self) -> None:
        super().__init__()
        self._database: DatabaseItem = DatabaseItem()
        self._type: str = 'item_correct'

    def _correcting_itens_file(self) -> None:
        correct_item = CorrectItem(self._param.path)
        correct_item.save_correct_itens()

    def run(self) -> None:
        #self._correcting_itens_file()
        super().run()

    def _process_df_rule(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["issued"] = pd.to_datetime(df["issued"])
        df["modified"] = pd.to_datetime(df["modified"])
        df["history"] = df["history"].str.replace(' ', '', regex=False)
        return df