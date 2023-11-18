import nltk
import yake
import regex as re
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_ru')
from pymystem3 import Mystem

ms = Mystem()


FILTER_CHARS = [
    ')', '(', ',', '!', ' .', ':', '|', '>', '<', '*', '[', ']', '...', './', '/\n', '\xa0',
    '«', '»', '_', '?', '~', '=', '\\', ';', '\n', '``', "''", '✅', '/n', '/', '..', '.', '`', "'", '-',
    '✔', '⇒', '"', '$', '%', '&', "'", ',', '^', '`', '{', '}', "('", '. ', ' . ',
]

stop_words = nltk.corpus.stopwords.words('russian') + nltk.corpus.stopwords.words('english')
exclude = [x for x in set(stop_words + FILTER_CHARS) if len(x) > 0]
def process_item(x: str):
    for char in FILTER_CHARS:
        x = x.replace(char, ' ').lower()
    item = ' '.join(re.split(r'(\d+)', x))
    while item.count(2 * " ") > 0:
        item = item.replace(2 * " ", " ")
    return item.strip(' ').replace(' и ', ' ')


def process(x):
    words = nltk.word_tokenize(x)
    words = [process_item(word) for word in words if word not in exclude]

    lemmetized = []
    for word in words:
        lemmetized.append(' '.join(ms.lemmatize(word)).strip(' \n'))

    return process_item(' '.join(lemmetized))


kw_extractor = yake.KeywordExtractor(
    lan='ru',
    n=2,
    dedupLim=0.9,
    dedupFunc='seqm',
    windowsSize=2,
    top=2,
    features=None
)


def extract(x):
    keywords = kw_extractor.extract_keywords(process(x))
    if len(keywords) > 0:
        return [str(x[0]) for x in keywords]
    elif len(keywords) == 0:
        return ''


def check_adj(x):
    if len(x.split()) > 1:
        return x
    else:
        spec = nltk.pos_tag([x], lang='rus')
        if len(spec) == 1:
            if spec[0][1] == 'A=m':
                return spec[0][1]
            else:
                return spec[0][0]
        else:
            return x
