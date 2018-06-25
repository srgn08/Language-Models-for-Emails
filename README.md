
# Project Title:

Implement Unigram, Bigram and Trigram models, and calculate probability and perplexity for each models.

# Running the tests:

The program needs 2 arguments for its operation. These are the name of the input file and the name of the output file.
The input file should be given in .txt format.

# Sample run code:
python3 assignment1.py datasets.txt results.txt

# The tasks of this project:

- Creation of Unigram, bigram and trigram models.
- Calculation of the probabilities of test mails using the trigram model we created and the laplace smoothing method.
 - Producing new mails according to created 3 different models.
 - Calculation of perplexity using testaments, bigram and trigram models.
 - Calculation of the perplexity of test mails using bigram and trigram models.
 
 
#  Information about the program:
 
 - The results produced by the program will be printed to the output file.
 - When generating program, 2nd input file taken for sample input (datasets.txt)
 - The results are calculated by taking the logarithm of the base 10 when probability calculation is performed using laplace smoothing according to three different models.
 - The format of the statements written to the output file is written according to utf-8.
 
 
 # Average duration of the program:
 
 -It takes about 2-3 minutes to do all the operations in a file with 100,000 data.
 
 Authors: Sergen Topcu