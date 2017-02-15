from nltk.corpus import brown, stopwords
from nltk import ConditionalFreqDist


cfd = ConditionalFreqDist()


# get a list of all English stop words
stopwords_list = stopwords.words('english')
stopwords_list

# define a function that returns true if the input tag is some form of noun
def is_noun(tag):
    return tag.lower() in ['nn','nns','nn$','nn-tl','nn+bez',\
                           'nn+hvz', 'nns$','np','np$','np+bez','nps',\
                           'nps$','nr','np-tl','nrs','nr$']


# count nouns that occur within a window of size 5 ahead of other nouns
for sentence in brown.tagged_sents():
	for (index, tagtuple) in enumerate(sentence):
		(token, tag) = tagtuple
		token = token.lower()
		if token not in stopwords_list and is_noun(tag):
			window = sentence[index+1:index+5]
			for (window_token, window_tag) in window:
				window_token = window_token.lower()
				if window_token not in stopwords_list and is_noun(window_tag):
					cfd[token].inc(window_token)

					




                
