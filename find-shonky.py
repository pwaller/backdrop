import pymongo

backdrop = pymongo.Connection()['backdrop']

for collection_name in backdrop.collection_names():
    if collection_name.endswith('monitoring') or collection_name.endswith('realtime'):
        continue
    collection = backdrop[collection_name]

    records = list(collection.find())

    for record in records:
        if '_timestamp' in record and record['_timestamp'].hour == 23:
            print(collection_name)
            break

