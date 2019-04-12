import scipy
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.corpus import stopwords
# from nltk.stem.wordnet import WordNetLemmatizer
import codecs
import utils as U
import pandas as pd
import jieba
import ast

def cleanData(domain, filename):
    with open('stopwords.txt') as f:
        content = f.readlines()
    stopwords = [x.strip() for x in content]
    # for i in range(len(stopwords)):
    #   stopwords[i] = stopwords[i]
    clean = []
    fname = './datasets/'+domain+'/' + filename
    df = pd.read_excel(fname)
    # df = df.dropna() #remove empty cells
    for line in df['QTYJ']:
        l = []
        seglist = jieba.cut(line, cut_all = False)
        for word in seglist:
            flag = True
            # wordlist = []
            if (word not in stopwords):
                for ch in word:
                    if ord(ch) < 0x4e00 or ord(ch) > 0x9fff:
                        flag = False
                        break
                if flag == True:
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
    # print(text_rmstop)
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
    # f1 = codecs.open('../datasets/'+domain+'/test.xlsx', 'r', 'utf-8')
    # f2 = codecs.open('../datasets/'+domain+'/test_label.xlsx', 'r', 'utf-8')
    f1 = U.read_file('./datasets/'+domain+'/test.xlsx')
    f2 = U.read_file('./datasets/'+domain+'/test_label.xlsx')

    out1 = codecs.open('./preprocessed_data/'+domain+'/test.txt', 'w', 'utf-8')
    out2 = codecs.open('./preprocessed_data/'+domain+'/test_label.txt', 'w', 'utf-8')

    for text, label in zip(f1, f2):
        # labelList = ast.literal_eval(label)
        # label = label.strip()
        textList = ast.literal_eval(text)
        tokens = parseSentence(textList)
        # if len(tokens) > 0:
        if len(label) != 1:
            out1.write(' '.join(tokens) + '\n')
            out2.write(label + '\n')

def preprocess(domain):
    print ('\t'+domain+' train set ...')
    preprocess_train(domain)
    print ('\t'+domain+' test set ...')
    preprocess_test(domain)


# cleanData('2014-2015', 'test.xlsx')
# cleanData('2014-2015', 'train.xlsx')
print ('Preprocessing raw review sentences ...')
preprocess('2014-2015')
# preprocess('restaurant')
