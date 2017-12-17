from pymongo import MongoClient

class __client:

	def __init__ (self):
		self._client = MongoClient()
	
	def setUp (self, db):
		self._db = self._client[db]
		self._name_db = db

	def drop (self):
		self._client.drop_database(self._db)
	
	def __getitem__(self, key):
		return self._db [key]

client = __client ()
client.setUp ('ait_judge')

from lang import lang
from solution import solution
from task import task
from contest import contest
from homework import homework
from user import user
from checker import checker
from test import test

checkers = client['checkers']
langs = client['langs']
solutions = client['solutions']
tasks = client['tasks']
contests = client['contests']
homework = client['homework']
users = client['users']
tests = client['tests']

def init_contests ():
	all_langs = langs.insert_many ([
		# Compile langs
		lang('C','c','c_cpp','gcc -O2 -Wall -std=c11 {} -o {} -static','./{}').to_object(),
		lang('C++','cpp','c_cpp','g++ -O2 -Wall -std=c++14 {} -o {} -static','./{}').to_object(), 
		# Script langs
		lang('Python','py','python','cp {} {}','python {}').to_object(),
		lang('Node.JS','js','javascript','cp {} {}','node {}').to_object(),
	]).inserted_ids;

	all_checkers = checkers.insert_many ([
		checker ('diff', 'diff (out1) (out2)').to_object (),
		checker ('diff - ignore all white space', 'diff -w (out1) (out2)').to_object (),
	]).inserted_ids

	all_tests = tests.insert_many ([
		test ('', '2').to_object (),
		test ('', '3').to_object (),
	]).inserted_ids
	
	curr_tasks = tasks.insert_many ([
		task ('1+1', '# 1+1\nPrint the result of 1+1 on the standart output.', [all_tests [0]], all_checkers [0], True).to_object (),
		task ('1+2', '# 1+2\nPrint the result of 1+2 on the standart output.', [all_tests [1]], all_checkers [1], False).to_object (),
	]).inserted_ids
	
	curr_contests = contests.insert_many ([
		# Active
		contest ('The director\'s cake - group X', [all_langs [0], all_langs [1]], "2017-04-12 12:30", "2018-04-12 16:30", curr_tasks).to_object (),
		contest ('The director\'s cake - group Y', [all_langs [0], all_langs [1]], "2017-04-12 12:30", "2018-04-12 16:30", []).to_object (),
		contest ('The director\'s cake - group Z', [all_langs [0], all_langs [1]], "2017-04-12 12:30", "2018-04-12 16:30", []).to_object (),
		# Past
		contest ('The director\'s cake', all_langs, "2014-04-12 12:30", "2014-04-12 16:30", []).to_object (),
		contest ('The director\'s cake', all_langs, "2014-04-12 12:30", "2014-04-12 16:30", []).to_object (),
		# Future
		contest ('The director\'s cake', all_langs, "2021-04-12 12:30", "2021-04-12 16:30", []).to_object (),
		contest ('The director\'s cake', all_langs, "2021-04-12 12:30", "2021-04-12 16:30", []).to_object (),
	]).inserted_ids
	
	solutions.insert_many ([
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
		solution (curr_contests [0], curr_tasks [0], users.find_one ({})['_id'], '', 'py').to_object (),
	])

def init ():
	langs = client['langs']
	solutions = client['solutions']
	tasks = client['tasks']
	contests = client['contests']
	homework = client['homework']
	users = client['users']
	users.insert_many ([
		user ('Alex Tsvetanov', 'alexts', 'alex@tsalex.tk', 'tts2002').to_object (),
	])
	init_contests ()

init ()
