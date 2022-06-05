# Author: Firas Moosvi
# Date: 2022-06-04

"""Convert one question.

Usage: 
    convertq.py [--instructor=<bool>] [--public=<bool>] [--prairielearn=<bool>] <source_root>

Arguments:
    source_root                Directory containing md source file.

Options:
    --instructor=<bool>        Exports md version of question.
    --public=<bool>            Exports md version of question with the answers removed.
    --prairielearn=<bool>      Exports info.json, server.py, and question.html.
"""

from docopt import docopt
import pathlib
import sys
import numpy as np
import os
import yaml
import problem_bank_scripts as pbs
    
def main():
    args = docopt(__doc__)
    
    source_root = args['<source_root>']

    questions = []
    for root, dirs, files in os.walk(source_root):
        for file in files:
            if(file.endswith(".md")):
                questions.append(os.path.join(root,file))
                pathlib.Path(source_root).mkdir(parents=True, exist_ok=True)
    
    # Read Question Files
    for source_filepath in questions:
        try:
            print(source_filepath)
            if args['--instructor']:
                pbs.process_question_md(source_filepath, instructor=True)

            if args['--public']:
                pbs.process_question_md(source_filepath, instructor=False)
                
            if args['--prairielearn']:
                pbs.process_question_pl(source_filepath)

        except Exception as e :
            print(f"There is an error in this problem: \n\t- File path: {source_filepath}\n\t- Error: {e}")
            raise e

if __name__ == '__main__':
    main()