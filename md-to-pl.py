# Author: Graham Bovett and Firas Moosvi
# Date: 2021-05-16

"""Processes all questions.

Usage: 
    md-to-pl.py <input_file> <output_path>
"""
import problem_bank_scripts as pbs
import docopt

def main():

    args = docopt.docopt(__doc__)

    input_file = args['<input_file>']
    output_path = args['<output_path>']

    pbs.process_question(input_file,output_path)

if __name__ == '__main__':

    main()