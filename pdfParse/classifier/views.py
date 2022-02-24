from django.shortcuts import render
from pdfParse.settings import UPLOAD_DIR, STATIC_URL
from .forms import UploadFileForm
from nltk.corpus.reader import wordnet
from nltk.corpus import wordnet
from pdfminer.high_level import extract_text  # extract text from pdf
import yake  # natural language processing module


def parse_pdf(request, pdfName, context):
    try:
        # turning entire pdf into a string
        exctext = extract_text(str(pdfName))
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


    # appending synonyms of tags for each division['updated_tags]
    for div in Division_list:
        for tags in div.get('tags', None):
            if tags is not None:
                for syn in wordnet.synsets(tags):
                    for l in syn.lemmas():
                        if l.name() not in div["updated_tags"]:
                            div['updated_tags'].append(l.name().lower())
            else:
                print('invalid synonym')

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
        key_words = []
        for word in keywords:
            try:
                key_words.append(word[0].lower())
            except Exception as e:
                print(e)
        # matching keywords
        matches = {}
        matched_words = []
        for div in Division_list:
            matches[div['division_name']] = 0

        for div in Division_list:
            for tag in div['updated_tags']:
                for words in keywords:
                    if (tag in words) or (tag == words):
                        matches[div['division_name']] += 1
                        count = matches[div['division_name']]
                        matched_words.append(words[0])
        max_match = max(matches, key=matches.get)
        context['matched_words'] = matched_words
        context['max_match'] = max_match
        context['tag_count'] = matches[context['max_match']]
    else:
        print("No text found or error while extracting text from pdf")
    return render(request, 'classifier/home.html', context)



def home(request):
    form = UploadFileForm()
    context = {'form': form}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file_name = form.instance.file
            parse_pdf(request, file_name, context)
        form = UploadFileForm()
    return render(request, 'classifier/home.html', context)

# Create your views here.
