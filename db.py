from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient()

def toobject (obj):
	a = obj
	a.pop ('_id', None)
	return a

def get_task ():
	sol = client ['ait_judge']['solutions'].find_one({'points': float('nan')})
	if sol == None:
		return None
	
	return {
		'id': str (sol ['_id']),
		'code': sol ['code'],
		'lang': sol ['lang'],
		'tests': [
			toobject (client['ait_judge']['tests'].find_one ({'_id': ObjectId(x)}))
				for x in client ['ait_judge']['tasks'].find_one({
						'_id': ObjectId(sol ['task_id'])
				})['tests']
		],
		'checker': toobject(client['ait_judge']['checkers'].find_one ({
				'_id': ObjectId (client ['ait_judge']['tasks'].find_one(
						{'_id': ObjectId (sol ['task_id'])}
					)['checker'])
		})),
	}

def update_task (id, points):
	client ['ait_judge']['solutions'].update_one ({'_id': ObjectId(id)}, {"$set": {'points': points, 'label': ''}}, upsert=False)

def update_partial_task (id, status):
	client ['ait_judge']['solutions'].update_one ({'_id': ObjectId(id)}, {"$set": {'label': status}}, upsert=False)
