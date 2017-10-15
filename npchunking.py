import nltk
from os.path import expanduser
from nltk.tag.senna import SennaTagger


#text = """Although the employees at Exponentia Datalabs are hardworking and sincere they lack potential to do something"""
#text = """you need to improve your customer support"""



#text = """no way to contact their customer service."""
#text = 'Samsung Galaxy S5 is a great mobile phone. One of the best batteries in terms of longevity. The processor as well as RAM is more than enough. A great buy'
#text = '''Although Samsung Galaxy S5 is a great phone, its battery does not last long'''
#text = """he got the nicer watch"""
#text = """Although it is a great phone, XpressMusic is expensive"""
#text = """Altough the restaurant boasted of good service, the food was pathetic"""
#text = """Dubai without adventure is a good option"""
#text = """Although Tom was mischievous, he was a good boy"""
#text = """What an idiot!"""
#text = """It was a good restaurant and bar"""
#text = 'The song is a blessing in disguise'
#text = 'What a waste of time'
#text = """The dog lived in the garden, but the cat, who was smarter, lived inside the house."""
# Used when tokenizing words
#text = """The good food eclipsed  the pathetic service"""
#text = """My neighbour watered the flowers"""
text = """The flowers were watered by my neighbour"""
#text = """Iphone is a good phone"""
#text = """If you sometimes like to go to the movies, Wasabi is a good place to start"""
#text = """I also believe that Dark Angel will become a cult favorite."""
#text = """Speed and bandwidth is good with symmetric upload and download"""
#text = 'debit card limit Debit Card Limit'
"""Texts it does not work properly on"""
#text = """If this series, over the last 16 years, has taught us anything, it's that just when you think it's about to run out of gas, it gets outfitted with an even more elaborate fuel-injection system"""
#text = """ The following things are not at all entertaining: The bad sound, the lack of climax and, worst of all, watching Seinfeld (who is also one of the film's producers) do everything he can to look like a good guy."""
#text = """Although it starts off so bad that ` you feel like running out screaming, it eventually works its way up to merely bad rather than painfully awful."""
#text = """An enigmatic film that's too clever for its own good, it's a conundrum not worth solving."""
#text= """"""

"""------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''

lemmatizer = nltk.WordNetLemmatizer()
#stemmer = nltk.stem.porter.PorterStemmer()

"""------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

#Su Nam Kim Paper
grammar = r"""

    #Adjectices with determinants and multiple adjectives    
    ADJ:
    {<JJ.*>*<CC>*<IN>*<JJ.*> | <DT>*<JJ.*><JJ.*>*} 
    
       
    # Nouns and Adjectives, terminated with Nouns
    NBAR:
    {<DT><NN.*> | <NN.*> | <NN.*>*<NN.*> | <NN.*><CC><NN.*> | <CD><NN.*>}  
       

    # Above, connected with in/of/etc...
    NP:
    {<NBAR><IN><NBAR> | <NBAR><RB>*<IN>*<NBAR>* | <ADJ><NBAR>}      
    

    VP:
    {<MD><VB.*> | <VB.*><IN>* | <DT><VB.*>}
    # Verbs and verbs with determinants
    
    VERBTO:
    {<VP><ADJ>*<TO><VP>}
    
    PHRASE:
    {<PRP.*>*<NP>*<VP><IN>*<NP> | <NP><NBAR>*<VP><ADJ><NBAR>* | <PRP.*><WDT>*<RB><WRB>*<RB>*<VP>*<NP>*<VP><NP><RB>* |<PRP.*><RB.*>*<VERBTO><PRP.*>*<TO><NBAR><NP>* | <PRP.*><RB.*>*<VERBTO><PRP.*>*<TO>*<NBAR>*<NP>* | <PRP.*>*<NP>*<RB>*<TO>*<VP>*<PRP.*><NP>*<RB>*<ADJ>*<NBAR>*<TO>*<NP>*<VP>*}
    
    
"""
 
"""------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

home = expanduser("~")
st = SennaTagger(home+'/senna')
chunker = nltk.RegexpParser(grammar)
#toks = nltk.regexp_tokenize(text, sentence_re)

#postoks = nltk.tag.pos_tag(text.split())
postoks = st.tag(text.split())

tree = chunker.parse(postoks)
tree.draw()
print tree
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

"""------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

'''
Extract leaves of noun & verb phrases from the tree
'''
def leaves(tree):
    """
    Finds NP (nounphrase) leaf nodes of a chunk tree.
    """
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
#        print type(subtree)
        yield subtree.leaves()


def leaves_verb(tree):
    """
    Finds NP (nounphrase) leaf nodes of a chunk tree.
    """
    for subtree in tree.subtrees(filter = lambda t: t.label()=='VP'):
#        print type(subtree)
        yield subtree.leaves()
    

def phrases(tree):
    """
    Finds separate phrases in a sentence
    """
    for subtree in tree.subtrees(filter = lambda t:t.label()=='PHRASE'):
        yield subtree.leaves()


def normalise(word):
    """
    Normalises words to lowercase and stems and lemmatizes it.
    """
    #word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word


def acceptable_word(word):
    """
    Checks conditions for acceptable word: length, stopword.
    """
    accepted = bool(2 <= len(word) <= 40)
#        and word.lower() not in stopwords)
    return accepted

def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w)]
        yield term

def get_verbterms(tree):
    for leaf in leaves_verb(tree):
        term = [ w for w,t in leaf if acceptable_word(w)]
        yield term
    
terms = get_terms(tree)
terms_verbs = get_verbterms(tree)
phrases(tree)
print '\nProbable Subject/Object(s):'
for term in terms:
    print ''
    for word in term:
        print word, 

print '\n'

print 'Probable Predicate(s):'
for term in terms_verbs:
    print '    '
    for word in term:
        print word, 
