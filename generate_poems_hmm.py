########################################
# CS/CNS/EE 155 2017
# Problem Set 5
#
# Author:       Avishek Dutta
# Description:  Set 5
########################################

from HMM import HiddenMarkovModel
import pickle as pkl

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
#    word2num = data['word2num']
    num2word = data['num2word']
    
    # Print file information.
    print("{:30}".format('Generated Emission'))
    print('#' * 70)
    print(HMM_file_path)
    print('')

    # Generate lines of sonnet
    for i in range(n_lines):
        emission, states = HMM.generate_emission(n_syllables, word2syllable, 
                                                 num2word)
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
        for N_iters in [100, 1000]:
            # create file path to HMM data
            HMM_file_path = HMM_file_prefix + str(n_states) + "_states_" + \
                str(N_iters) + "_iters.pkl"
            # generate sonnet
            sonnet_generator(HMM_file_path)
