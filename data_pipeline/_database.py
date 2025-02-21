import psycopg2
from _utils import print_status

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
            print_status(f"recreated successfully - {table_name}")
        except psycopg2.Error as e:
            self.conn.rollback()  # Rollback in case of error
            print_status(f"Error recreating table `{table_name}`: {e}")

class DatabaseTrain(Database):
    def __init__(self):
        super().__init__()
        self.columns_explode = ["history", "timestampHistory", "numberOfClicksHistory", "timeOnPageHistory", "scrollPercentageHistory", "pageVisitsCountHistory", "timestampHistory_new"]

    def recreate_table(self):
        schema_sql = """
        create table if not exists table_train (
            userid text,
            usertype text,
            historysize int,
            history text,
            timestamphistory timestamp,
            numberofclickshistory int,
            timeonpagehistory int,
            scrollpercentagehistory float,
            pagevisitscounthistory int,
            timestampHistory_new timestamp
        );
        """
        super().recreate_table("table_train", schema_sql)

    def insert_table(self):
        insert_query = """
        insert into table_train (
            userid, usertype, historysize, history, timestamphistory,
            numberofclickshistory, timeonpagehistory, scrollpercentagehistory, 
            pagevisitscounthistory, timestampHistory_new
        ) values %s
        """
        return insert_query

class DatabaseItem(Database):
    def __init__(self):
        super().__init__()    

    def recreate_table(self):
        schema_sql = """
        create table if not exists table_item (
            page text,
            url text,
            issued timestamp,
            modified timestamp,
            title text,
            body text,
            caption text
        );
        """
        super().recreate_table("table_item", schema_sql)

    def insert_table(self):
        insert_query = """
        insert into table_item (
            page, url, issued, modified, title, body, caption
        ) values %s
        """
        return insert_query
    
class DatabaseFull(Database):
    def __init__(self):
        super().__init__()

    def table_full(self) -> None:
        schema_sql = """
        select
            a.*,
            b.*,
            now() as create_timestamp
        into table_full
        from table_train as a
        left join table_item as b
            on a.history = b.page
        """        
        super().recreate_table("table_full", schema_sql)