# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 19:48:14 2019

@author: Josef M Sabuda
"""
from HMM import HiddenMarkovModel
import PreprocessingMethods as PM
import pickle as pkl
import random

n_states = 16
n_iters = 1000
HMM_file_prefix = 'data/HMM_data_'
HMM_file_path = HMM_file_prefix + str(n_states) + "_states_" + str(n_iters) + "_iters_rhyming.pkl"

# generate limericks
n_lines=5
n_syllables=9
    
# load data
with open(HMM_file_path, 'rb') as f:
    data = pkl.load(f)

# extract data
HMM = data['HMM']
word2syllable = data['word2syllable']
#    syllable2word = data['syllable2word']
word2num = data['word2num']
num2word = data['num2word']
    
# Print file information.
print("{:30}".format('Generated Emission'))
print('#' * 70)
print(HMM_file_path)
print('')

# select last words that rhyme without replacement
a = []
while len(a) != 3:
    rhyming_pairs = PM.generate_list_of_rhymes(word2num)
    selected_rhyming_pairs = [p[1] for p in random.sample(list(enumerate(rhyming_pairs)), int(n_lines/2))]

    a = list(selected_rhyming_pairs[0])
    b = a[1]
    c = a[0]
    d = selected_rhyming_pairs[1]

    for i in range(1072):
        if (str(rhyming_pairs[i][0]) == b) & (str(rhyming_pairs[i][1]) != c):
            a.append(rhyming_pairs[i][1])
            break
        elif (str(rhyming_pairs[i][1]) == b) & (str(rhyming_pairs[i][0]) != c):
            a.append(rhyming_pairs[i][0])
            break
            
selected_rhyming_pairs = [tuple(a),d]

# initialize list of last words
last_word_list = ['' for i in range(n_lines)]
    
#Fill in list of last words
last_word_list[0] = selected_rhyming_pairs[0][0]
last_word_list[1] = selected_rhyming_pairs[0][1]
last_word_list[2] = selected_rhyming_pairs[1][0]
last_word_list[3] = selected_rhyming_pairs[1][1]
last_word_list[4] = selected_rhyming_pairs[0][2]  

# Generate lines of the lymerick
for i in range(2):
    emission, states = HMM.generate_emission(n_syllables, word2syllable, 
                                             num2word, 
                                             last_word=word2num[last_word_list[i]])
    x = ''.join([word + ' ' for word in emission])
    x = x.capitalize().strip()
    # Print the results.
    print("{:30}".format(x))


for i in range(2,4):
    emission, states = HMM.generate_emission(6, word2syllable, 
                                             num2word, 
                                             last_word=word2num[last_word_list[i]])
    x = ''.join([word + ' ' for word in emission])
    x = x.capitalize().strip()
    # Print the results.
    print("{:30}".format(x))

for i in range(4,5):
    emission, states = HMM.generate_emission(n_syllables, word2syllable, 
                                             num2word, 
                                             last_word=word2num[last_word_list[i]])
    x = ''.join([word + ' ' for word in emission])
    x = x.capitalize().strip()
    # Print the results.
    print("{:30}".format(x))


print('')
print('')