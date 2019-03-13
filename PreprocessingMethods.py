# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 16:01:01 2019

@author: Andy
"""

import pickle as pkl

def generate_syllable_dictionaries(filepath="data/Syllable_dictionary.txt",
                                   delim=' ', max_syllables=5):
    """
    Generates dictionaries of words to syllables and syllables to words from
    given data file.
    Inputs:
        filepath : String giving filepath to syllable dictionary file. Default is
                    filepath to syllable dictionary given in the project folder.
    
    Outputs:
        word2syllable : dictionary providing a list of the possible numbers of 
                        syllables given a word (string).
        syllable2word : dictionary providing a list of words with a given number
                        of syllables
    """
    # initialize dictionaries
    word2syllable = {}
    syllable2word = {}
    
    # initialize lists of words for each possible number of syllables
    for i in range(max_syllables+1):
        # normal
        syllable2word[str(i)] = []
        # ending (will always be at least 1 fewer than max syllables)
        if i < max_syllables:
            syllable2word['E'+str(i)] = []
    
    # initialize dictionaries of words to numbers and numbers to words
    word2num = {}
    num2word = {}
    
    # load file
    with open(filepath, 'r') as f:
        
        while True:
            # read line-by-line
            line = f.readline()
            # stop reading if reached end of file
            if not line:
                break
            
            # tokenize line and split into words and syllables
            tokens = line.strip().split(delim)
            word = tokens[0]
            syllables = tokens[1:]
            
            # save to dictionaries
            word2syllable[word] = syllables
            for s in syllables:
                syllable2word[s] += [word]
            num = len(word2num)
            word2num[word] = num
            num2word[num] = word
    
    return word2syllable, syllable2word, word2num, num2word

def tokenize_sonnets(dictionary, filepath="data/shakespeare.txt", 
                     chars_2_remove='!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~'):
    """
    Tokenizes sonnets into individual words.
    Inputs:
        filepath : path to text file containing sonnets.
    Outputs:
        X : list of lists lines from sonnets, which are tokenized as lists of
            words (no punctuation) 
    """
    # initialize training data structure
    X = []
    
    # load file
    with open(filepath, 'r') as f:
        
        while True:
            # read line-by-line
            line = f.readline()
            # stop reading if reached end of file
            if not line:
                break
            
            # tokenize
            tokens = line.split(' ')
            # process tokens to generate data samples
            processed_tokens = []
            # loop through all words s
            for s in tokens:
                # remove punctuation and spacing from word (***TODO: figure out how to incorporate it)
                s = s.translate(str.maketrans('', '', chars_2_remove)).strip()
                # if there is a word left after stripping of punctuation and spacing
                # that is NOT a number...
                if len(s) > 0 and not s.isdigit():
                    # make lowercase
                    s = s.lower()
                    # ...check if the word is in the dictionary
                    if s not in dictionary:
                        # if not, try removing apostrophes (might be used as
                        # quotation marks)
                        s = s.translate(str.maketrans('','', "'"))
                        # MAKE SURE WORD IS IN DICTIONARY
                        assert s in dictionary, "missing word: %s" % s
                        
                    # having found word in dictionary, add its index to sequence
                    processed_tokens += [dictionary[s]]
                    
            # add to data samples if it contains at least two tokens
            if len(processed_tokens) > 1:
                X += [processed_tokens]
            
    return X
    
if __name__ == "__main__":
    dicts = generate_syllable_dictionaries()
    word2num = dicts[2]
    X = tokenize_sonnets(word2num)
#    with open('syllable_dictionaries.pkl', 'wb') as f:
#        pkl.dump(dicts, f)
