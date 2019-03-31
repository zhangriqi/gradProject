from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'/Users/zhangruiqi/Downloads/Learning/MachineLearning/stanford-corenlp-full-2018-10-05', lang = 'zh')

class MyTokenizer(object):
	def __init__(self):
		pass

	def tokenize(self, raw):
		return nlp.word_tokenize(raw)