########################################
# CS/CNS/EE 155 2017
# Problem Set 5
#
# Author:       Andrew Kang
# Description:  Set 5
########################################

from HMM import unsupervised_HMM
from HMM import HiddenMarkovModel
import PreprocessingMethods as PM

import pickle as pkl

def unsupervised_learning_rhyming(n_states, N_iters, save_prefix="data/HMM_data_",
                          print_matrices=False):
    '''
    Trains an HMM using supervised learning on the file 'ron.txt' and
    prints the results.

    Arguments:
        n_states:   Number of hidden states that the HMM should have.
    '''
    word2syllable, syllable2word, word2num, num2word = PM.generate_syllable_dictionaries()
    sonnet_lines = PM.tokenize_sonnets(word2num)

    # Train the HMM on sequences in reverse
    HMM = unsupervised_HMM(sonnet_lines, n_states, N_iters, backwards=True)

    data2save = {}
    data2save['HMM'] = HMM
    data2save['word2syllable'] = word2syllable
    data2save['syllable2word'] = syllable2word
    data2save['word2num'] = word2num
    data2save['num2word'] = num2word
    
    # save results
    save_path = save_prefix + str(n_states) + "_states_" + str(N_iters) + "_iters_rhyming.pkl"
    with open(save_path, 'wb') as f:
        pkl.dump(data2save, f)
        
    if print_matrices:
        # Print the transition matrix.
        print("Transition Matrix:")
        print('#' * 70)
        for i in range(len(HMM.A)):
            print(''.join("{:<12.3e}".format(HMM.A[i][j]) for j in range(len(HMM.A[i]))))
        print('')
        print('')
    
        # Print the observation matrix. 
        print("Observation Matrix:  ")
        print('#' * 70)
        for i in range(len(HMM.O)):
            print(''.join("{:<12.3e}".format(HMM.O[i][j]) for j in range(len(HMM.O[i]))))
        print('')
        print('')

if __name__ == '__main__':
    print('')
    print('')
    print('#' * 70)
    print("{:^70}".format("Running HMM for Shakespearean Sonnets"))
    print('#' * 70)
    print('')
    print('')

    for n_states in [4,8]:
        for N_iters in [100]:
            unsupervised_learning(n_states, N_iters)
