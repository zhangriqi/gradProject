"""
Currently dummy extraction that only extracts the Noun phrases.
"""
import nltk
import re
import sys
sys.path.append('/Users/zhangruiqi/Downloads/test/gradProject/transformers/ABAEModel/pre_trained_model/2014-2015')

class SentenceAspectExtractor():

    def __init__(self):
        pass

    def get_sent_aspects(self, sentence):
        """
        INPUT: a sentence object
        OUTPUT: a list of the features extracted from the given sentence
        """
        tagged_sent = sentence.pos_tagged
        NPS = self.get_NPs(tagged_sent)
        return aspects 

    def get_NPs(self, tagged_sent):
        NPs = []
        for t_sent in tagged_sent:
            for wordTag in t_sent:
                if wordTag[1] == "NN" or wordTag[1] == "NR" or wordTag[1] == "NT":
                    if wordTag[0] not in NPs:
                        NPs.append(str(wordTag[0]))
        return NPs 

    def group_

class ABAEAspectExtractor():
    def get_sent_aspects(self, sentence):
        """
        INPUT: a sentence object
        OUTPUT: a list of the features extracted from the given sentence
        """
        true = open('/Users/zhangruiqi/Downloads/test/gradProject/transformers/ABAEModel/pre_trained_model/2014-2015/predict_out.txt')
        pred_aspects = []
        for line in true:
            pred_aspects.append(line.strip())
        return pred_aspects 