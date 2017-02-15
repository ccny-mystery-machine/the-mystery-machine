import nltk


# Sentences Segment
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
paragraph = "Alice went to Bob'home. Alice killed Bob"
sentences = sent_tokenizer.tokenize(paragraph)
sentences

#Tokenize sentences
words = WordPunctTokenizer().tokenize(paragraph)
words


#part-of-speech tagging, like adjective, noun
def sentence_pos(sentences):
    for sent in sentences:
        words = nltk.pos_tag(sent)
        print words
