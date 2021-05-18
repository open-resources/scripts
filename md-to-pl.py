# Author: Graham Bovett and Firas Moosvi
# Date: 2021-05-16

"""Processes all questions.

Usage: 
    md-to-pl.py <input_file> <output_path>
"""

import docopt
import os
import uuid
import json
import pathlib
from problem_bank_scripts import problem_bank_scripts as pbs 

def write_info_json(output_path, parsed_question):
    """
    Args:
        output_path ([type]): [description]
        parsed_question ([type]): [description]
    """

    pathlib.Path(output_path / 'info.json').write_text("""{
            "uuid": \"""" + str(uuid.uuid4()) + """\",
            "title": \"""" + parsed_q['header']['title'] + """",
            "topic": \"""" + parsed_q['header']['topic'] + """",
            "tags":  """ + json.dumps(parsed_q['header']['tags']) + """,
            "type": "v3"
        }""")

def write_server_py(output_path,parsed_question):
    """
    Args:
        output_path ([type]): [description]
        parsed_question ([type]): [description]
    """
    
    try:
        imp, func = parsed_q['header']['server'].split('# Start problem code')
    except:
        raise
    
    (output_path / "server.py").write_text(imp+'def generate(data):'+func.replace('\n','\n\t'))

def process_multiple_choice(part_name,parsed_question, data_dict):
    """
    Args:
        output_path (Path): [description]
        parsed_question (dict): [description]
        data_dict (dict)
    
    Returns:
        str: Multiple choice question is returned as a string with PL-compliant syntax.
    """

    html = f"""<pl-question-panel>\n\t<p>{parsed_q['body_parts_split'][part_name]['content']}\t</p>\n</pl-question-panel>\n\n"""
    
    pl_customizations = " ".join([f'{k} = "{v}"' for k,v in parsed_question['header'][part_name]['pl-customizations'].items()]) # PL-customizations
    html += f"""<pl-multiple-choice answers-name="{part_name}" {pl_customizations} >\n"""

    for ans in data_dict['params'][f'{part_name}'].keys():
        html += f"\t<pl-answer correct= |@ params.{part_name}.{ans}.correct @| > |@ params.part{part_name}.{ans}.value @| |@ params.{part_name}.units @| </pl-answer>\n"

    html += '</pl-multiple-choice>\n' 

    return replace_tags(html)

def process_checkbox():
    return 5

def process_number_input():
    return 5

def process_symbolic_input():
    return 5

def replace_tags(string):
    """Takes in a string with tags: |@ and @| and returns {{ and }} respectively. This is because Python strings can't have double curly braces.

    Args:
        string (str): String to be processed, can be multi-line.

    Returns:
        string (str): returns string with tags replaced with curly braces.
    """
    return string.replace('|@','{{').replace('@|','}}')

def main():

    args = docopt.docopt(__doc__)
    try:
        input_file = pathlib.Path(args['<input_file>'])
    except:
        print("File does not exist.")
        raise

    output_path = pathlib.Path(args['<output_path>'])

    # ## Types of questions
    SINGLE = ['number-input']
    MULTIPLE = ['multiple-choice', 'checkbox']

    # Parse the MD file
    parsed_q = pbs.read_md_problem(input_file)

    # Create output dir if it doesn't exist
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    ############### Start Sketchiest Part
    # Run the python code
    exec(parsed_q['server'],globals())
    exec('generate(data)')
    ############### End Sketchiest Part

    # Write info.json file
    write_info_json(output_path, parsed_q)

    # Prepare question.html
    question_html = ""

    ##### single part

    question_html += process_multiple_choice('part1',parsed_question,data)



    ##### Multi part

    mp1 = """
    <div class="card my-2">
    \t<div class="card-header">\n
    \t\t{part_name}
    \t</div>\n
    \n
    \t<div class="card-body">\n
    \n
    """



    # if parsed_q['num_parts'] == 1:

    #     part_name = 'part1'
    #     q_type = parsed_q['header'][part_name]['type'] # Question Type

    #     if 'multiple-choice' in q_type:

    #         # process_multiple_choice()
    #         pass

    #     elif 'number-input' in q_type:

    #         # process_number_input()
    #         pass

    #     elif 'checkbox' in q_type:

    #         # process_checkbox()
    #         pass

    #     elif 'symbolic_input' in q_type:

    #         # process_symbolic_input()
    #         pass



    else:

        for i in range(1, parsed_q['num_parts'] + 1):
            part_name = f'part{i}' # Part Name
            q_type = parsed_q['header'][part_name]['type'] # Question Type
            pl_customizations = parsed_q['header'][part_name]['pl_customizations'] # PL-customizations

            #q_txt, ans_section = parsed_q['body_parts'][part_name].split('### Answer Section')      

            question_html += '<p><b>' + q_txt[2:q_txt.index('\n')].strip() + '</b></p>\n' +\
                        '<p style="margin-left: 15px">' + q_txt[q_txt.index('\n'):] + '</p>\n'

            #answer = parsed_q['header'][part_name]['instructor_answers']

            if q_type in SINGLE:
                question_html += '<pl-' + q_type + ' answers_name="' + answer + '"' + pl_customizations + '>\n'
            elif q_type in MULTIPLE:
                question_html += '<pl-' + q_type + ' answers_name="' + part_name + '"' + pl_customizations + '>\n'
                for ans in data['params'][f'part{part_name}'].keys():
                    question_html += f"\t<pl-answer correct= |@ params.{part_name}.{ans}.correct @| > |@ params.part{part_name}.{ans}.value @| |@ params.{part_name}.units @| </pl-answer>\n"
                
                question_html += '</pl-answer>\n'
            else:  # other element types, such as images, that require their own formatting
                raise NotImplementedError
            question_html += '</pl-' + q_type + '>\n'

            if i < parsed_q['num_parts']:
                question_html +='<hr/>\n'


    # Write question.html file

    (output_path / "question.html").write_text(question_html)

    # Write server.py file
    (output_path / "server.py").write_text(parsed_q['header']['server'])

    # TODO: Find and move any image assets 

if __name__ == '__main__':

    main()