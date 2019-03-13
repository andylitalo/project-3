# project-3
+PreprocessingMethods.py is a library of methods for preprocessing the data.
Used by generate_poems_hmm.py and unsupervised_hmm.py

+HMM.py is a library of methods to train an HMM based on HW6 solutions.
Used by generate_poems_hmm.py and unsupervised_hmm.py

+unsupervised_hmm.py is a script that trains an HMM with the given number of hidden states (n_states) and iterations (N_iters). Saves data as HMM_data_#_states_#_iters.pkl

+generate_poems_hmm.py is a script that loads one of the data files saved by unsupervised_hmm.py and generates a 14-line sonnet with 10 syllables per line

+HMM_data_#_states_#_iters.pkl are data files where the first number gives the number of hidden states and the second number gives the number of iterations. Saved by unsupervised_hmm.py and loaded by generate_poems_hmm.py
