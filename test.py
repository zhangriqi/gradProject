import pandas as pd
import sys
sys.path.append('/Users/zhangruiqi/Downloads/test/gradProject/classes')
# from review import Review
from teacher import Teacher

def get_reviews_for_teacher(t_id, df):
	return df[df['GH'] == t_id]

def preprocess_xlsx(sourcefile, destfile):
    df1 = pd.read_excel(sourcefile)
    writer = pd.ExcelWriter(destfile)
    df2 = df1.dropna() #remove empty cells
    df2.to_excel(writer, 'Sheet1', index = False)
    writer.save()

def read(filename):
	print('processing')
	df = pd.read_excel(filename)
	print(df.GH.unique()) #returns a list
	print(df.ZWMC.iloc[1])
	t_ids = df.GH.unique()

	for t_id in t_ids:
		tea = Teacher(get_reviews_for_teacher(t_id, df))
		# print(tea.review)

		summary = tea.aspect_based_summary()
		print(summary, type(summary))

print('testing...')
read("Data.xlsx")
