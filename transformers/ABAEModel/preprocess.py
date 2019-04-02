import scipy
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.corpus import stopwords
# from nltk.stem.wordnet import WordNetLemmatizer
import codecs
import utils as U
import pandas as pd
import jieba
import ast

def cleanData(domain):
    with open('stopwords.txt') as f:
        content = f.readlines()
    stopwords = [x.strip() for x in content]
    # for i in range(len(stopwords)):
    #   stopwords[i] = stopwords[i]
    clean = []
    fname = './datasets/'+domain+'/train.xlsx'
    df = pd.read_excel(fname)
    for line in df['QTYJ']:
        l = []
        seglist = jieba.cut(line, cut_all = False)
        for word in seglist:
            # wordlist = []
            if (word not in stopwords):
                l.append(word)
        clean.append(l)
    df['clean'] = clean
    df.to_excel(fname, sheet_name = 'Sheet1')

def parseSentence(line):
    # lmtzr = WordNetLemmatizer()    
    with open('stopwords.txt') as f:
        content = f.readlines()
    stop = [x.strip() for x in content]
    # text_token = CountVectorizer().build_tokenizer()(line)
    # text_rmstop = [i for i in text_token if i not in stop]
    text_rmstop = [i for i in line if i not in stop]
    # text_stem = [lmtzr.lemmatize(w) for w in text_rmstop]
    # return text_rmstem
    print(text_rmstop)
    return text_rmstop


def preprocess_train(domain):
    # f = codecs.open('../datasets/'+domain+'/train.xlsx', 'r', 'utf-8')
    f = U.read_file('./datasets/'+domain+'/train.xlsx')
    out = codecs.open('./preprocessed_data/'+domain+'/train.txt', 'w', 'utf-8')

    for line in f:
    	tsList = ast.literal_eval(line)
    	tokens = parseSentence(tsList)
    	if len(tokens) > 0:
        	out.write(' '.join(tokens)+'\n')

def preprocess_test(domain):
    # For restaurant domain, only keep sentences with single 
    # aspect label that in {Food, Staff, Ambience}

    f1 = codecs.open('../datasets/'+domain+'/test.txt', 'r', 'utf-8')
    f2 = codecs.open('../datasets/'+domain+'/test_label.txt', 'r', 'utf-8')
    out1 = codecs.open('../preprocessed_data/'+domain+'/test.txt', 'w', 'utf-8')
    out2 = codecs.open('../preprocessed_data/'+domain+'/test_label.txt', 'w', 'utf-8')

    for text, label in zip(f1, f2):
        label = label.strip()
        if domain == 'restaurant' and label not in ['Food', 'Staff', 'Ambience']:
            continue
        tokens = parseSentence(text)
        if len(tokens) > 0:
            out1.write(' '.join(tokens) + '\n')
            out2.write(label+'\n')

def preprocess(domain):
    print ('\t'+domain+' train set ...')
    preprocess_train(domain)
    # print '\t'+domain+' test set ...'
    # preprocess_test(domain)


cleanData('2014-2015')
print ('Preprocessing raw review sentences ...')
preprocess('2014-2015')
# preprocess('beer')