import psycopg2

class Database:
    def __init__(self):
        self.conn = self._get_connection()
        self.cursor = self.conn.cursor()

    def _get_connection(self):
        return psycopg2.connect(
            dbname="globo",
            user="postgres",
            password="admin1234",
            host="localhost",
            port="5432"
        )

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def recreate_table(self, table_name, schema_sql):
        try:
            drop_table_sql = f"DROP TABLE IF EXISTS {table_name};"
            self.cursor.execute(drop_table_sql)
            self.cursor.execute(schema_sql)
            self.conn.commit()
            print(f"Table `{table_name}` recreated successfully.")
        except psycopg2.Error as e:
            self.conn.rollback()  # Rollback in case of error
            print(f"Error recreating table `{table_name}`: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DatabaseTrain(Database):
    def __init__(self):
        super().__init__()
        self.columns_explode = ["history", "timestampHistory", "numberOfClicksHistory", "timeOnPageHistory", "scrollPercentageHistory", "pageVisitsCountHistory"]

    def recreate_table(self):
        schema_sql = """
        CREATE TABLE IF NOT EXISTS table_train (
            userId TEXT,
            userType TEXT,
            historySize INT,
            history TEXT,
            timestampHistory BIGINT,
            numberOfClicksHistory INT,
            timeOnPageHistory INT,
            scrollPercentageHistory FLOAT,
            pageVisitsCountHistory INT
        );
        """
        super().recreate_table("table_train", schema_sql)

    def insert_table(self):
        insert_query = """
        INSERT INTO table_train (
            userId, userType, historySize, history, timestampHistory,
            numberOfClicksHistory, timeOnPageHistory, scrollPercentageHistory, pageVisitsCountHistory
        ) VALUES %s
        """
        return insert_query

class DatabaseItem(Database):
    def __init__(self):
        super().__init__()    

    def recreate_table(self):
        schema_sql = """
        CREATE TABLE IF NOT EXISTS table_item (
            page TEXT,
            url TEXT,
            issued TEXT,
            modified TEXT,
            title TEXT,
            body TEXT,
            caption TEXT
        );
        """
        super().recreate_table("table_item", schema_sql)

    def insert_table(self):
        insert_query = """
        INSERT INTO table_item (
            page, url, issued, modified, title, body, caption
        ) VALUES %s
        """
        return insert_query