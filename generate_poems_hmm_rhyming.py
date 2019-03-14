########################################
# CS/CNS/EE 155 2017
# Problem Set 5
#
# Author:       Avishek Dutta
# Description:  Set 5
########################################

from HMM import HiddenMarkovModel
import pickle as pkl
import random

def sonnet_generator(HMM_file_path, n_lines=14, n_syllables=10):
    '''
    Generates n_lines of n_syllables the HMM stored in the file given by the
    file path and prints the results.

    Arguments:
        HMM_file_path: directory to file containing HMM data
        n_lines: number of lines to generate (14 to follow Shakespeare)
        n_syllables: number of syllables per line (10 to follow Shakespeare)
    '''
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

    # select last words that rhyme according to ababcdcdefefgg without replacement
    rhyming_pairs = PM.generate_list_of_rhymes(word2num)
    selected_rhyming_pairs = [p[1] for p in random.sample(list(enumerate(rhyming_pairs)), int(n_lines/2))]
    
    # initialize list of last words
    last_word_list = ['' for i in range(n_lines)]
    
    # define which lines must rhyme
    rhyming_lines_list = [(0,2),(1,3),(4,6),(5,7),(8,10),(9,11),(12,13)]
    
    # sample last words that rhyme
    for i in range(len(rhyming_lines_list)):
        l1, l2 = rhyming_lines_list[i]
        r1, r2 = selected_rhyming_pairs[i]
        last_word_list[l1] = r1
        last_word_list[l2] = r2
    
    # Generate lines of sonnet
    for i in range(n_lines):
        emission, states = HMM.generate_emission(n_syllables, word2syllable, 
                                                 num2word, 
                                                 last_word=word2num[last_word_list[i]])
        x = ''.join([word + ' ' for word in emission])
        x = x.capitalize().strip()

        # Print the results.
        print("{:30}".format(x))

    print('')
    print('')

if __name__ == '__main__':
    print('')
    print('')
    print("#" * 70)
    print("{:^70}".format("Generating Poems with HMM"))
    print("#" * 70)
    print('')
    print('')
    
    HMM_file_prefix = 'data/HMM_data_'
    for n_states in [4,8]:
        for N_iters in [100]:
            # create file path to HMM data
            HMM_file_path = HMM_file_prefix + str(n_states) + "_states_" + \
                str(N_iters) + "_iters_rhyming.pkl"
            # generate sonnet
            sonnet_generator(HMM_file_path)
