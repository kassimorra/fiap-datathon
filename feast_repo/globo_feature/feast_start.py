from feast import FeatureStore
from datetime import datetime
from _globo import globo, globo_fv

print('Defining featureStore path')
fs = FeatureStore(repo_path=".")

print('Apply globo feature')
fs.apply([globo, globo_fv])

print('Materialize globo feature')
start = datetime(2020,1,1)
end = datetime(2025,12,31)
fs.materialize(start, end)