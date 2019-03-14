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
            word, syllables = get_word_and_syllables(line, delim)
            
            # save to dictionaries
            word2syllable[word] = syllables
            for s in syllables:
                syllable2word[s] += [word]
            num = len(word2num)
            word2num[word] = num
            num2word[num] = word
    
    # TODO Might only need num2word and word2syllable
    return word2syllable, syllable2word, word2num, num2word

def get_word_and_syllables(line, delim):
    """
    Returns word and list of possible number of syllables given a line from the
    syllable dictionary.
    """
    tokens = line.strip().split(delim)
    word = tokens[0]
    syllables = tokens[1:]
            
    return word, syllables


def tokenize_sonnets(dictionary, filepath="data/shakespeare.txt", 
                     chars_2_remove='!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~'):
    """
    Tokenizes sonnets into individual words.
    Inputs:
        dictionary : dictionary from words to indices from 0 to D - 1, where D
                        is the total number of words.
        filepath : path to text file containing sonnets.
        chars_2_remove : string of characters to remove from words, mostly
                            punctuation, but keeps ' and - by default
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
            # process words to generate data samples
            processed_words = []
            # loop through all words s
            for s in tokens:
                # remove punctuation and spacing from word (***TODO: figure out how to incorporate it)
                s = remove_symbols(s, chars_2_remove)
                # if there is a word left after stripping of punctuation and spacing
                # that is NOT a number...
                if len(s) > 0 and not s.isdigit():
                    processed_words += [process_word(s, dictionary)]                   
                    
            # add to data samples if it contains at least two tokens
            if len(processed_words) > 1:
                X += [processed_words]
            
    return X


def remove_symbols(s, chars_2_remove, remove_whitespace=True):
    """
    Removes desired characters from given string s. Also remvoes whitespace by
    default.
    """
    result = s.translate(str.maketrans('', '', chars_2_remove))
    if remove_whitespace:
        result = result.strip()
        
    return result
    
def process_word(s, dictionary):
    """
    Processes given word before adding its index to data list.
    Dictionary is a dictionary from words to coresponding indices, which range 
    from 0 to D-1, where D is the total number of words.
    """
    # make lowercase
    s = s.lower()
    # ...check if the word is in the dictionary
    if s not in dictionary:
        # if not, try removing apostrophes (might be used as
        # quotation marks)
        s = remove_symbols(s, "'")
        # MAKE SURE WORD IS IN DICTIONARY
        assert s in dictionary, "missing word: %s" % s
        
    return dictionary[s]

def generate_list_of_rhymes(dictionary, filepath="data/shakespeare.txt", 
                     chars_2_remove='!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~'):
    """
    Generates a list of pairs of rhyming words for producing rhyming sonnets.
    """
    # initialize list of rhyming pairs
    rhyme_list = []
    # initalize list of last words
    last_word_list = []
    
    # load file of sonnets
    with open(filepath, 'r') as f:
    
        # loop through sonnets
        while True:
            # read line-by-line
            line = f.readline()
            # stop reading if reached end of file
            if not line:
                break
            
            # check if there is a number, which indicates a new sonnet
            new_sonnet = any(char.isdigit() for char in line)
            # check if line is blank by removing all whitespace
            is_blank = len(line.strip()) == 0
            
            if new_sonnet:
                
                if len(last_word_list) == 0:
                    last_word_list = []
                    continue
                
                elif len(last_word_list) == 12:
                    # save last words in appropriate rhyming pairs ababcdcdefef
                    for i in [0, 1, 4, 5, 8, 9]:
                        rhyme_list += [(last_word_list[i], last_word_list[i+2])]
                    # initialize list of last words for new sonnet
                    last_word_list = []
                    
                elif len(last_word_list) == 14:  
                    # save last words in appropriate rhyming pairs ababcdcdefef
                    for i in [0, 1, 4, 5, 8, 9]:
                        rhyme_list += [(last_word_list[i], last_word_list[i+2])]
                    # last couplet gg
                    rhyme_list += [(last_word_list[12], last_word_list[13])]
                    # initialize list of last words for new sonnet
                    last_word_list = []
                
                elif len(last_word_list) == 15:
                        # save last words in appropriate rhyming pairs ababacdcdefef
                        # except for a's, which will be saved explicitly below
                        for i in [1, 5, 6, 9, 10]:
                            rhyme_list += [(last_word_list[i], last_word_list[i+2])]
                        # last couplet gg
                        rhyme_list += [(last_word_list[13], last_word_list[14])]
                        # add pairs from 1st, 3rd, and 5th lines
                        rhyme_list += [(last_word_list[0], last_word_list[2]),
                                       (last_word_list[0],last_word_list[4]),
                                       (last_word_list[2],last_word_list[4])]
                        # initialize list of last words for new sonnet
                        last_word_list = []
                
                else: 
                    print('Length of last word list is not accounted for, = %i' 
                          % len(last_word_list))  
                    
            # if not a new sonnet and not a blank line, load last word
             elif not is_blank:
                last_word_list += [get_last_word(line)] 
                
    return rhyme_list

def get_last_word(line, chars_2_remove='!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~'):
    """
    Returns the last word in a string of words.
    """
    # get last token
    last_token = line.split(' ')[-1]
    # remove punctuation and spacing from word (***TODO: figure out how to incorporate it)
    last_word = remove_symbols(last_token, chars_2_remove)
                
    return last_word


if __name__ == "__main__":
    dicts = generate_syllable_dictionaries()
    word2num = dicts[2]
    X = tokenize_sonnets(word2num)
    rhyming_pairs = generate_list_of_rhymes(word2num)
#    with open('syllable_dictionaries.pkl', 'wb') as f:
#        pkl.dump(dicts, f)
