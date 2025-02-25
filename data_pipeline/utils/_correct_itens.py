import pandas as pd
import re
import glob

class CorrectItem:
    def __init__(self, param_path: dict):
        self.param_path: dict = param_path
        self.uuid_pattern: re.Pattern[str] = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")    

    def _uuid_clean_lines(self, file_path: str) -> list[str]:
        rows: list[str] = []
        current_row: str = ""

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip("\n")
                if not line:
                    continue
                if self.uuid_pattern.match(line):
                    if current_row:
                        rows.append(current_row.replace("\n", " "))
                    current_row = line
                else:
                    current_row += " " + line

        if current_row:
            rows.append(current_row.replace("\n", " "))

        return rows[1:]

    def _split_rows(self, rows: list[str]) -> list[str]:
        data: list[str] = []
        for row in rows:
            parts = row.split(",", 4)
            uuid, page_url, issued, modified, news_concat = parts
            data.append([uuid.strip(), page_url, issued, modified, news_concat.strip()])
        return data

    def _list_to_df(self, data: list[str]) -> pd.DataFrame:
        return pd.DataFrame(data, columns=["history", "page_url", "issued", "modified", "news_concat"])

    def _clean_itens_part(self, itens_path: str) -> pd.DataFrame:   
        file_itens: list[str] = self._uuid_clean_lines(itens_path)
        split_list: list[str] = self._split_rows(file_itens)
        return self._list_to_df(split_list)

    def _save_new_csv(self, data: pd.DataFrame, idx: int) -> None:
        data.to_csv(f"./source_files/correct_itens/cleaned_file_{idx}.csv", index=False, encoding="utf-8", escapechar="\\")
        print(f"save sucessfull file -> cleaned_file_{idx}.csv")

    def save_correct_itens(self) -> None:
        _input: str = "item"
        for idx, fpath in enumerate(glob.glob(f"{self.param_path[_input]}")):
            dataframe: pd.DataFrame = self._clean_itens_part(fpath)
            self._save_new_csv(dataframe, idx)


