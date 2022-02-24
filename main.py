from nltk.corpus.reader import wordnet
from nltk.corpus import wordnet
from pdfminer.high_level import extract_text  # extract text from pdf
import yake #natural language processing module


# pdf parsing
try:
    exctext = extract_text('test.pdf')  # turning entire pdf into a string
except Exception as e:
    print(e)
Division_list = [
    {"division_name": "Map Division, Schwarzman",
     "tags": ["map", "Global", "US"],
     'updated_tags': ["map", "Global", "US"]
     },
    {"division_name": "Manuscripts, Archives & Rare Books, Schomburg",
     "tags": ["education", "learning", "schools", 'student', 'campus,'],
     "updated_tags": ["Education", "learning", "Schools"]
    }
]


#appending synonyms of tags for each division['updated_tags]
for div in Division_list:
    for tags in div.get('tags', None):
        if tags is not None:
            for syn in wordnet.synsets(tags):
                for l in syn.lemmas():
                    if l.name() not in div["updated_tags"]:
                        div['updated_tags'].append(l.name().lower())
        else:
            print('invalid synonym')
# [print(i.get('updated_tags')) for i in Division_list]
 

if(exctext):
    # Natural Language Processing
    # kw_extractor = yake.KeywordExtractor()  # initializing the keyword extractor
    max_ngram_size = 1  # maximum size of ngrams (size of keywords)
    deduplication_threshold = 0.90  # 90% probability
    numOfKeywords = 200  # number of keywords to extract
    custom_kw_extractor = yake.KeywordExtractor(lan="en", n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=numOfKeywords, features=None)  # setting the parameters of the keyword extractor
    keywords = custom_kw_extractor.extract_keywords(
        exctext)  # extracting keywords from the text
    [print(word[0]) for word in keywords[:10]]  # printing the keywords
    key_words = []
    for word in keywords:
        try:
            key_words.append(word[0].lower())
        except Exception as e:
            print(e)
    #matching keywords 
    matches = {}
    for div in Division_list:
        matches[div['division_name']] = 0

    for div in Division_list:
        for tag in div['updated_tags']:
            for words in keywords:
                if (tag in words) or (tag == words):
                    matches[div['division_name']] += 1
    max_match = max(matches , key=matches.get)
    print('\n', matches, '\n')
    print('\n', max_match, '\n')
else:
    print("No text found or error while extracting text from pdf")