from utils._utils import load_all
from utils._process import ProcessTrain, ProcessItem
from utils._database import DatabaseFull

# Load Train and Item folders
load_all(ProcessTrain, ProcessItem)

# Create the join table from train and item
database_full: DatabaseFull = DatabaseFull()
database_full.table_full()