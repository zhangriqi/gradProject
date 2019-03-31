# import nltk
from sentence import Sentence


class Review(object):
	def __init__(self, review_dict, teacher=None):
		self.review_class_id = review_dict['ZWMC'] #string
		self.user_id = review_dict['USER_XH'] #string
		self.text = review_dict['QTYJ']	#string	

		if teacher:
			self.teacher = teacher

		self.sentences = self.sentence_tokenize(self.text) #type = sentence.Sentence

	def sentence_tokenize(self, review_text):
		res =  [Sentence(review_text, review=self)]
		return res

	def __iter__(self):
		return self.sentences.__iter__()


	def __str__(self):
		return self.text

	