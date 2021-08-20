from flask import Flask
from flask import render_template
from flask import request

from nltk.tokenize import TreebankWordTokenizer
from collections import Counter
import copy
import math
from collections import OrderedDict


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/calculate', methods = ['POST', 'GET'])
def calculate():
    tokenizer = TreebankWordTokenizer()

    if(request.form['text_1'] == ""):
        return render_template('hello.html', error="Nu ati introdus primul text")
    if (request.form['text_2'] == ""):
        return render_template('hello.html', error="Nu ati introdus al doilea text")

    docs = []
    docs.append(request.form['text_1'])
    docs.append(request.form['text_2'])

    doc_tokens = []
    for doc in docs:
        doc_tokens += [sorted(tokenizer.tokenize(doc.lower()))]
    all_doc_tokens = sum(doc_tokens, [])
    lexicon = sorted(set(all_doc_tokens))
    zero_vector = OrderedDict((token, 0) for token in lexicon)
    doc_vector = []
    x = []
    for doc in docs:
        vec = copy.copy(zero_vector)

        tokens = tokenizer.tokenize(doc.lower())
        token_counts = Counter(tokens)
        for key, value in token_counts.items():
            vec[key] = value / len(lexicon)
            doc_vector.append(vec)
        x.append(vec)

    numerator = 0
    for key, value in x[0].items():
        numerator += x[1][key] * value

    first_text = 0
    for key, value in x[0].items():
        first_text += value ** 2

    second_text = 0
    for key, value in x[1].items():
        second_text += value**2


    denominator = math.sqrt(first_text) * math.sqrt(second_text)
    cousine = numerator / denominator

    return render_template('hello.html', response=cousine)
if __name__ == '__main__':
    app.run()