import json
import time
import pandas as pd
import sys
sys.path.append('/Users/zhangruiqi/Downloads/test/gradProject/classes')
from teacher import Teacher


def get_reviews_for_teacher(t_id, df):
	"""
	INPUT: teacher id, pandas DataFrame
	OUTPUT: Series with only texts
	
	For a given teacher id, return the review_id and text of all reviews for that teacher. 
	"""
	return df[df['GH'] == t_id]

def read_data(filename):
	"""
	INPUT: filename
	OUTPUT: pandas data frame from file
	"""
	return pd.read_excel(filename)

def main():
	df = read_data('testData.xlsx')
	# df.dropna()
	
	# summaries_coll = []
	t_ids = df.GH.unique()

	for t_id in t_ids:
		print ("Working on teacher %s" % t_id)

		tea = Teacher(get_reviews_for_teacher(t_id, df))
		summary = tea.aspect_based_summary()

		# summaries_coll.insert(summary)

		print ("Inserted summary for %s " % t_id)

if __name__ == "__main__":
	main()