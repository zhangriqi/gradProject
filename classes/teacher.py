from collections import Counter
from operator import itemgetter
import sys
sys.path.append('/Users/zhangruiqi/Downloads/test/gradProject/classes')
from review import Review
from transformers.sentiment import SentimentModel, OpinionModel

class Teacher(object):

	SENTIMENT_MODEL = SentimentModel()
	OPINION_MODEL = OpinionModel()

	def __init__(self, review_df):
		assert len(review_df['GH'].unique()) == 1, "Must pass data for a single teacher to Teacher"

		# Store business-level meta data
		self.teacher_id = str(review_df.GH.iloc[0]) # string 
		self.subject_name = str(review_df.ZWMC.iloc[0]) # string

		self.review = [Review(dict(review_row), teacher = self) for _, review_row in review_df.iterrows()]

	def __iter__(self):
		return self.review.__iter__()

	def __str__(self):
		return self.teacher_id

	def aspect_based_summary(self):
		aspects = self.extract_aspects()
		asp_dict = dict([(aspect, self.aspect_summary(aspect)) for aspect in aspects])

		# asp_dict = self.fiter_asp_dict(asp_dict) #filter aspects that don't have enough sentences, not finished yet

		return { 'teacher_id': self.teacher_id,
				 'class_name': self.subject_name,
				 'aspect_summary':asp_dict
		}

	def extract_aspects(self, single_word_thresh = 0.012, multi_word_thresh = 0.003):
		asp_sents = [sentences.aspects for review in self for sentences in review]
		n_sents = float(len(asp_sents))
		# return asp_sents
		single_asps = []
		multi_asps = []

		for sent in asp_sents:
			for asp in sent:
				if len(asp) == 1:
					single_asps.append(" ".join(asp))
				elif len(asp) > 1:
					multi_asps.append(" ".join(asp))
				else:
					assert(False), "somthing wrong with aspect extraction"

		single_asps = [(asp, count) for asp, count in Counter(single_asps).most_common(30) if count/n_sents > single_word_thresh]
		multi_asps = [(asp, count) for asp, count in Counter(multi_asps).most_common(30) if count/n_sents > multi_word_thresh]

		single_asps = self.filter_single_asps(single_asps, multi_asps)

		all_asps = [asp for asp,_ in sorted(single_asps + multi_asps, key=itemgetter(1))]

		# return self.filter_all_asps(all_asps)
		return all_asps


	def filter_single_asps(self, single_asps, multi_asps):
		return [(sing_asp, count) for sing_asp, count in single_asps if not any([sing_asp in mult_asp for mult_asp, _ in multi_asps])]



	def aspect_summary(self, aspect):
		OPIN_THRESH = 0.75
		HARD_MIN_OPIN_THRESH = 0.6

		POS_THRESH = 0.85
		NEG_THRESH = 0.85

		# override the opinion classifier if sentiment classifier is REALLY sure. 
		SENTI_OVERRIDE_THRESHOLD = .95 

		SENTENCE_LEN_THRESHOLD = 30 # number of words

		pos_sents = []
		neg_sents = []

		aspect_sents = self.get_sents_by_aspect(aspect)

		for sent in aspect_sents:

			if len(sent.tokenized) > SENTENCE_LEN_THRESHOLD:
				continue #filter really long sentences

			prob_opin = Teacher.OPINION_MODEL.get_opinionated_proba(sent)
			prob_pos = Teacher.SENTIMENT_MODEL.get_positive_proba(sent) 
			prob_neg = 1 - prob_pos

			sent_dict = sent.encode()
			sent_dict['prob_opin'] = prob_opin
			sent_dict['prob_pos'] = prob_pos
			sent_dict['prob_neg'] = prob_neg
			sent_dict['sorter'] = prob_opin*max(prob_pos, prob_neg) #used to order sentences for display

			if prob_opin > OPIN_THRESH or (max(prob_pos, prob_neg) > SENTI_OVERRIDE_THRESHOLD and prob_opin > HARD_MIN_OPIN_THRESH):
				if prob_pos > POS_THRESH:
					pos_sents.append(sent_dict)
				elif prob_neg > NEG_THRESH:
					neg_sents.append(sent_dict)

		n_sents = len(pos_sents) + len(neg_sents) if len(pos_sents) + len(neg_sents) > 0 else 1

		return {'pos': sorted(pos_sents, key=itemgetter('prob_pos'), reverse=True), # sort by confidence
				'neg': sorted(neg_sents, key=itemgetter('prob_neg'), reverse=True), # sort by confidence
				'num_pos': len(pos_sents),
				'num_neg': len(neg_sents),
				'frac_pos': len(pos_sents) / n_sents
				}

	def get_sents_by_aspect(self, aspect):
		return [sent for review in self for sent in review if sent.has_aspect(aspect)] 

