from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'/Users/zhangruiqi/Downloads/Learning/MachineLearning/stanford-corenlp-full-2018-10-05', lang = 'zh')

class MyTokenizer(object):
	def __init__(self):
		pass

	def tokenize(self, raw):
		return nlp.word_tokenize(raw)

def pos_tag(tokenized_sent):
		POS_sent = []
		for sent in tokenized_sent:
			taggedSent = nlp.pos_tag(sent)
			POS_sent.append(taggedSent)
		return POS_sent

if __name__ == '__main__':
	tok = MyTokenizer()
	samples = (
		# "What if it's English.",
		"现在正在测试中文分词?",
		# "如果是乱码呢？&……%¥"
		)
	for s in samples:
		print ("======================================================================")
		print (s)
		tokenized = tok.tokenize(s)
		# print ("\n".join(tokenized))
		print('pos_tag: ', pos_tag(tokenized))
		print('parse: , ', nlp.parse(s))

