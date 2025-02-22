from _utils import load_all
from _process import ProcessTrain, ProcessItem
from _database import DatabaseFull

# Load Train and Item folders
# load_all(ProcessTrain, ProcessItem)
# load_all(ProcessItem)

# Create the join table from train and item
database_full: DatabaseFull = DatabaseFull()
database_full.table_full()