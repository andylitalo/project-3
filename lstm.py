from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
from keras.utils import to_categorical
import numpy as np
from numpy import array


def sampling(preds,tem):
    preds=np.asarray(preds).astype('float64')
    preds=np.log(preds)/tem
    preds=np.exp(preds)/np.sum(np.exp(preds))
    prob=np.random.multinomial(1,preds,1)
    return np.argmax(prob)


with open('data/shakespeare.txt') as f:
  lines = [line.strip(' ').lower() for line in f]
  #lines = [line.strip('\n') for line in lines]
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
   
sonnetnew=[]     
for poem in sonnets:
    newline=[]
    for line in poem:
        newstr = line.replace("\n", "")
        newline.append(newstr)
    sonnetnew.append(newline)
sonnets=sonnetnew


wordlen=40
layer=1
chars=sorted(set([c for s in sonnets for l in s for c in l]))
text=''.join([c for s in sonnets for l in s for c in l])
char2indices=dict((c,i) for i, c in enumerate(chars))
indices2char=dict((i,c) for i, c in enumerate(chars))

sentences=[]
next_chars=[]
for i in range(0,len(text)-wordlen):
    sentences.append(text[i:i+wordlen])
    next_chars.append(text[i+wordlen])


mapping=dict((c, i) for i, c in enumerate(chars))

sequences = list()
for line in sentences:
	encoded_seq = [mapping[char] for char in line]
	sequences.append(encoded_seq)

vocab_size = len(mapping)

sequences = array(sequences)
x, y = sequences[:,:-1], sequences[:,-1]

sequences = [to_categorical(a, num_classes=vocab_size) for a in x]
x = array(sequences)
y = to_categorical(y, num_classes=vocab_size)


model = Sequential()
model.add(LSTM(256, input_shape=(x.shape[1], x.shape[2]), return_sequences=layer>1))
for i in range(1, layer):
    model.add(LSTM(256, return_sequences=i<(layer-1)))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

model.fit(x, y,batch_size=128,epochs=600,initial_epoch=0)


for tem in [0.25, 0.75, 1.5]:
    print('temperature:', tem)

    generated = ''
    sentence = "shall i compare thee to a summer's day?"
    generated += sentence
    print('Generating with seed: "' + sentence + '"')

    for i in range(700):
        x_pred=np.zeros((1, wordlen, len(chars)))
        for t,char in enumerate(sentence):
            x_pred[0,t,char2indices[char]]=1.0
        preds=model.predict(x_pred, verbose=0)[0]
        next_index=sampling(preds,tem)
        next_char=indices2char[next_index]

        generated=generated+next_char
        sentence=sentence[1:] + next_char
    print(generated)
    
    
