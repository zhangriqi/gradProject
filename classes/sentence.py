import nltk
import numpy as np
from stanfordcorenlp import StanfordCoreNLP

from transformers.tokenizers import MyTokenizer
from transformers.asp_extractors import SentenceAspectExtractor
nlp = StanfordCoreNLP(r'/Users/zhangruiqi/Downloads/Learning/MachineLearning/stanford-corenlp-full-2018-10-05', lang = 'zh')

class Sentence(object):
	WORD_TOKENIZER = MyTokenizer()

	ASP_EXTRACTOR = SentenceAspectExtractor()

	def __init__(self, raw, review=None):
		self.raw = raw #string
		self.tokenized = self.word_tokenize(raw) #list of strings tokenized into words
		self.pos_tagged = self.pos_tag(self.tokenized) #list of tuples

		if review: #if passed, store a reference to the review this came from
			self.review = review
		self.aspects = self.compute_aspects() #[['老师'],'学的']]

	def __str__(self):
		return self.raw

	def word_tokenize(self, raw):
		return Sentence.WORD_TOKENIZER.tokenize(raw)

	def pos_tag(self, tokenized_sent):
		POS_sent = []
		for sent in tokenized_sent:
			taggedSent = nlp.pos_tag(sent)
			POS_sent.append(taggedSent)
		return POS_sent

	def compute_aspects(self):
		return Sentence.ASP_EXTRACTOR.get_sent_aspects(self)

	def has_aspect(self, asp_string):
		asp_toks = asp_string.split(" ")
		return all([tok in self.tokenized for tok in asp_toks])

	def encode(self):
		return {'text': self.raw,
				'user': self.review.user_id
				}




