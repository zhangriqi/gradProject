'''
Currently dummy extraction that only extracts the Noun phrases.

'''
class SentenceAspectExtractor():

    def __init__(self):
        pass

    def get_sent_aspects(self, sentence):
    	'''
    	INPUT: a sentence object
    	OUTPUT: a list of the features extracted from the given sentence
    	'''
        tagged_sent = sentence.pos_tagged
        aspects = self.get_NPs(tagged_sent)
        return aspects 

    def get_NPs(self, tagged_sent):
        NPs = []
        for t_sent in tagged_sent:
            for wordTag in t_sent:
                if wordTag[1] == "NN" or wordTag[1] == "NR" or wordTag[1] == "NT":
                    if wordTag[0] not in NPs:
                        NPs.append(str(wordTag[0]))
        return NPs 

