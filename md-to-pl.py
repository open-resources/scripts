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
#from problem_bank_scripts.src 
import problem_bank_scripts as pbs 

def write_info_json(output_path, parsed_question):
    """
    Args:
        output_path ([type]): [description]
        parsed_question ([type]): [description]
    """

    pathlib.Path(output_path / 'info.json').write_text("""{
            "uuid": \"""" + str(uuid.uuid4()) + """\",
            "title": \"""" + parsed_question['header']['title'] + """",
            "topic": \"""" + parsed_question['header']['topic'] + """",
            "tags":  """ + json.dumps(parsed_question['header']['tags']) + """,
            "type": "v3"
        }""")

def write_server_py(output_path,parsed_question):
    """
    Args:
        output_path ([type]): [description]
        parsed_question ([type]): [description]
    """
    
    try:
        imp, func = parsed_question['header']['server'].split('# Start problem code')
    except:
        raise

    func = func.replace('read_csv("','read_csv(data["options"]["client_files_course_path"]+"/')
    func = func.replace('\n','\n    ')

    (output_path / "server.py").write_text(imp+'def generate(data):'+func)

def process_multiple_choice(part_name,parsed_question, data_dict):
    """Processes markdown format multiple-choice questions and returns PL HTML
    Args:
        output_path (Path): [description]
        parsed_question (dict): [description]
        data_dict (dict)
    
    Returns:
        str: Multiple choice question is returned as a string with PL-compliant syntax.
    """

    html = f"""<pl-question-panel>\n\t<p>{parsed_question['body_parts_split'][part_name]['content']}\t</p>\n</pl-question-panel>\n\n"""
    
    pl_customizations = " ".join([f'{k} = "{v}"' for k,v in parsed_question['header'][part_name]['pl-customizations'].items()]) # PL-customizations
    html += f"""<pl-multiple-choice answers-name="{part_name}_ans" {pl_customizations} >\n"""

    if data_dict['params'][f'vars']['units']:
        units = f"|@ params.vars.units @|"
    else:
        units = ''

    for ans in data_dict['params'][f'{part_name}'].keys():
        html += f"\t<pl-answer correct= |@ params.{part_name}.{ans}.correct @| > |@ params.{part_name}.{ans}.value @| {units} </pl-answer>\n"

    html += '</pl-multiple-choice>\n' 

    return replace_tags(html)

def process_dropdown(part_name,parsed_question, data_dict):
    """Processes markdown format dropdown questions and returns PL HTML

    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        html: A string of HTML that is part of the final PL question.html file.
    """

    raise NotImplementedError

def process_number_input(part_name,parsed_question, data_dict):
    """Processes markdown format number-input questions and returns PL HTML

    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        html: A string of HTML that is part of the final PL question.html file.
    """

    html = f"""<pl-question-panel>\n\t<p>{parsed_question['body_parts_split'][part_name]['content']}\t</p>\n</pl-question-panel>\n\n"""
    
    pl_customizations = " ".join([f'{k} = "{v}"' for k,v in parsed_question['header'][part_name]['pl-customizations'].items()]) # PL-customizations
    html += f"""<pl-number-input answers-name="{part_name}_ans" {pl_customizations} ></pl-number-input>\n"""

    return replace_tags(html)

def process_checkbox(part_name,parsed_question, data_dict):
    """Processes markdown format checkbox (select all that apply) questions and returns PL HTML

    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        html: A string of HTML that is part of the final PL question.html file.
    """
    # start with the MCQ version and then...change things for checkbox questions
    html = process_multiple_choice(part_name,parsed_question, data_dict).replace('-multiple-choice','-checkbox')
    return html

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

    output_path = pathlib.Path(args['<output_path>']) / input_file.parts[-2]

    # Parse the MD file
    parsed_q = pbs.read_md_problem(input_file)

    # Create output dir if it doesn't exist
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    ############### Start Sketchiest Part
    # Run the python code
    exec(parsed_q['header']['server'].split('# Update the data object with a new dict')[0],globals())
    ############### End Sketchiest Part

    # Write info.json file
    write_info_json(output_path, parsed_q)

    ## Single part questions

    if parsed_q['num_parts'] == 1:
        q_type = parsed_q['header']['part1']['type']
        if 'multiple-choice' in q_type:
            question_html = process_multiple_choice('part1',parsed_q,data2)
        elif 'number-input' in q_type:
            question_html = process_number_input('part1',parsed_q,data2)
        elif 'checkbox' in q_type:
            question_html = process_checkbox('part1',parsed_q,data2)

        elif 'symbolic_input' in q_type:
            # process_symbolic_input()
            pass

    ##### Multi part
    else:
        question_html = ""
        for pnum in range(1, parsed_q['num_parts'] + 1):
            part = 'part'+f'{pnum}'
            q_type = parsed_q['header'][part]['type']

            question_html += f"""
                <div class="card my-2">
                \t<div class="card-header">
                \t{parsed_q['body_parts_split'][part]['title']}
                </div>\n
                <div class="card-body">\n\n\n
                """
            if 'multiple-choice' in q_type:                
                question_html += f"{process_multiple_choice(part,parsed_q,data2)}"  
            elif 'number-input' in q_type:
                question_html += f"{process_number_input(part,parsed_q,data2)}"
            elif 'checkbox' in q_type:
                question_html = process_checkbox('part1',parsed_q,data2)
            elif 'symbolic_input' in q_type:
                # process_symbolic_input()
                pass

            question_html += "</div>\n</div>\n\n"

    # Write question.html file

    (output_path / "question.html").write_text(question_html)

    # Write server.py file
    write_server_py(output_path,parsed_q)

    # TODO: Find and move any image assets 

if __name__ == '__main__':

    main()