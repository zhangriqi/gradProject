import gensim
import codecs
import pandas as pd

class MySentences(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for line in codecs.open(self.filename, 'r', 'utf-8'):
            yield line.split()

def main(domain):
    source = './preprocessed_data/%s/train.txt' % (domain)
    model_file = './preprocessed_data/%s/w2v_embedding' % (domain)
    # source = './preprocessed_data/%s' %(fname)
    # model_file = './preprocessed_data/w2v_embedding'
    sentences = MySentences(source)
    model = gensim.models.Word2Vec(sentences, size=50, window=5, min_count=1, workers=4)
    # model.wv.save_word2vec_format(fname="vectors.txt", fvocab=None, binary=False)
    # print (model.similar_by_vector(model["老师"], topn=1))
    model.save(model_file)

print ('Pre-training word embeddings ...')
main('2014-2015')
# main('beer')