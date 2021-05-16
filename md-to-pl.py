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
import md_parser
import pathlib

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
    parsed_q = md_parser.parse(input_file)

    # Create output dir if it doesn't exist
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    # Write info.json file
    pathlib.Path(output_path / 'info.json').write_text("""{
            "uuid": \"""" + str(uuid.uuid4()) + """\",
            "title": \"""" + parsed_q['header']['title'] + """",
            "topic": \"""" + parsed_q['header']['topic'] + """",
            "tags":  """ + json.dumps(parsed_q['header']['tags']) + """,
            "type": "v3"
        }""")

    # Write question.html file
    question_html = ""
    for i in range(1, parsed_q['num_parts'] + 1):
        part_name = 'part{0}'.format(i)
        q_txt, ans_section = parsed_q['body'][part_name].split('### Answer Section')
        q_type = parsed_q['header'][part_name]['type']
        pl_options = ''

        question_html += '<p><b>' + q_txt[2:q_txt.index('\n')].strip() + '</b></p>\n' +\
                    '<p style="margin-left: 15px">' + q_txt[q_txt.index('\n'):] + '</p>\n'

        answer = parsed_q['header'][part_name]['instructor_answers']

        if q_type in SINGLE:
            question_html += '<pl-' + q_type + ' answers_name="' + answer + '"' + pl_options + '>\n'
        elif q_type in MULTIPLE:
            question_html += '<pl-' + q_type + ' answers_name="' + part_name + '"' + pl_options + '>\n'
            choices = [s.strip() for s in ans_section.split('-')]
            del choices[0]

            if type(answer) != list:
                answer = [answer]
            for choice in choices:
                question_html += '\t<pl-answer correct="' +\
                            str(any(ans in choice for ans in answer)) + '">' +\
                            choice + '</pl-answer>\n' 
        else:  # other element types, such as images, that require their own formatting
            pass
        question_html += '</pl-' + q_type + '>\n'

        if i < parsed_q['num_parts']:
            question_html +='<hr/>\n'

    (output_path / "question.html").write_text(question_html)

    # Write server.py file
    server_py = ""

    server_info = parsed_q['header']['server']  # isolate server info
    eoi_index = server_info.index('\n', server_info.rindex("import"))
    server_py += server_info[:eoi_index].strip() + "\n\ndef generate(data):\n\t" + \
                server_info[eoi_index:].strip().replace('\n', '\n\t') + "\n"  # add generate method

    # TODO: add generate() to the YAML file ?

    (output_path / "server.py").write_text(server_py)

    # TODO: Find and move any image assets 

if __name__ == '__main__':

    main()