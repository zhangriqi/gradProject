import gensim
# import codecs
import pandas as pd
import jieba

class MySentences(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        df = pd.read_excel(self.filename)
        for line in df['clean']:
        # for line in codecs.open(self.filename, 'r', 'utf-8'):
            yield line.split()
def cleanData(fname):
    with open('stopwords.txt') as f:
        content = f.readlines()
    stopwords = [x.strip() for x in content]
    # for i in range(len(stopwords)):
    #   stopwords[i] = stopwords[i]
    clean = []
    df = pd.read_excel(fname)
    for line in df['QTYJ']:
        l = []
        seglist = jieba.cut(line, cut_all = False)
        for word in seglist:
            wordlist = []
            if (word not in stopwords):
                wordlist.append(word)
                l.append(wordlist)
        clean.append(l)
    df['clean'] = clean
    df.to_excel(fname, sheet_name = 'Sheet1')

def main(fname):
    # source = '../preprocessed_data/%s/train.txt' % (domain)
    # model_file = '../preprocessed_data/%s/w2v_embedding' % (domain)
    source = './preprocessed_data/%s' %(fname)
    model_file = './preprocessed_data/w2v_embedding'
    sentences = MySentences(source)
    model = gensim.models.Word2Vec(sentences, size=50, window=5, min_count=5, workers=4)
    model.save(model_file)

print ('Pre-training word embeddings ...')
cleanData('./preprocessed_data/Data.xlsx')
main('Data.xlsx')
# main('beer')