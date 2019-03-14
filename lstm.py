from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
import numpy as np
import sys


def _sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


with open('data/shakespeare.txt') as f:
  lines = [line.strip(' ').lower() for line in f]
sonnets = []
ln_start = 0
ln_end = 0
for ln, content in enumerate(lines):
    if content[:-1].isdigit():
        ln_start = ln + 1
    elif not content[:-1]:
        if ln - 1 == ln_end:
            sonnets.append(lines[ln_start:ln_end + 1])
    elif ln + 1 == len(lines):
        sonnets.append(lines[ln_start:ln_end + 1])
    else:
        ln_end = ln
        
wordlen=40
layer=1
chars = sorted(set([c for s in sonnets for l in s for c in l]))
text = ''.join([c for s in sonnets for l in s for c in l])
char_indices = dict((c, i) for i, c in enumerate(chars))

step = 1
sentences = []
next_chars = []
for i in range(0, len(text) - wordlen, step):
    sentences.append(text[i: i + wordlen])
    next_chars.append(text[i + wordlen])
print('nb sequences:', len(sentences))

x = np.zeros((len(sentences), wordlen, len(chars)))
y = np.zeros((len(sentences), len(chars)))
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


model = Sequential()
model.add(LSTM(256, input_shape=(wordlen, len(chars)), return_sequences=layer>1))
for i in range(1, layer):
    model.add(LSTM(256, return_sequences=i<(layer-1)))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')


model.fit(x, y,batch_size=128,epochs=600,initial_epoch=0)




indices_char = dict((i, c) for i, c in enumerate(chars))

for diversity in [0.25, 0.75, 1.5]:
    print('----- temperature:', diversity)

    generated = ''
    sentence = "shall i compare thee to a summer's day?\n"
    generated += sentence
    print('----- Generating with seed: "' + sentence + '"')
    #sys.stdout.write(generated)

    for i in range(670):
        x_pred = np.zeros((1, wordlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.0

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = _sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

        #sys.stdout.write(next_char)
        #sys.stdout.flush()
    sys.stdout.write(generated)
    print()