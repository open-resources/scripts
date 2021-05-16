import os
import uuid
import json
import md_parser

# TODO: validity checking for customizations
ALLOWED_CUSTOMIZATIONS = {'multiple-choice': ['answers-name', 'weight', 'inline', 'number-answers', 'fixed-order',
                                              'hide-letter-keys', 'all-of-the-above', 'none-of-the-above',
                                              'external-json', 'external-json-correct-key',
                                              'external-json-incorrect-key'],
                          'checkbox': ['answers-name', 'weight', 'inline', 'number-answers', 'min-correct',
                                       'max-correct', 'fixed-order', 'partial-credit', 'partial-credit-method',
                                       'hide-help-text', 'detailed-help-text', 'hide-answer-panel', 'hide-letter-keys',
                                       'hide-score-badge'],
                          'number-input': ['answers-name', 'weight', 'correct-answer', 'label', 'suffix', 'display',
                                           'comparison', 'rtol', 'atol', 'digits', 'allow-complex', 'allow-blank',
                                           'blank-value', 'show-help-text', 'show-placeholder', 'size',
                                           'show-correct-answer', 'allow-fractions']}

# TODO: add rest of types
SINGLE = ['number-input']
MULTIPLE = ['multiple-choice', 'checkbox']

# Create input and output file directories if they DNE
try:
    os.mkdir("question_templates")
    input("> Place MD question files in 'question_templates' folder.\n"
          "> Press Enter to continue\n")
except FileExistsError:
    pass
try:
    os.mkdir("PL-questions")
except FileExistsError:
    pass

# Check for question inputs
_, _, filenames = next(os.walk("question_templates"))
if not filenames:
    input("> Question source folder empty\n"
          "> Press Enter to quit\n")
    quit()

# Process questions
for q_name in filenames:
    parsed_q = md_parser.parse("question_templates/" + q_name)

    # Create output dir
    out_dir = 'PL-questions/' + parsed_q['header']['title']
    try:
        os.mkdir(out_dir)
    except FileExistsError:
        pass

    # Writing to files
    # Creating info.json file
    with open(out_dir + "/info.json", 'w') as info:
        info.write("""{
            "uuid": \"""" + str(uuid.uuid4()) + """\",
            "title": \"""" + parsed_q['header']['title'] + """",
            "topic": \"""" + parsed_q['header']['topic'] + """",
            "tags":  """ + json.dumps(parsed_q['header']['tags']) + """,
            "type": "v3"
        }""")

    # Creating question.html file
    with open(out_dir + "/question.html", 'w') as question:
        for i in range(1, parsed_q['num_parts'] + 1):
            part_name = 'part{}'.format(i)
            q_txt, ans_section = parsed_q['body'][part_name].split('### Answer Section')
            q_type = parsed_q['header'][part_name]['type']
            pl_options = ''
            # TODO: keyerror handling for wrong types
            for key in parsed_q['header'][part_name]['pl-customizations']:
                if key in ALLOWED_CUSTOMIZATIONS[q_type]:
                    pl_options += ' ' + key + '="' + str(parsed_q['header'][part_name]['pl-customizations'][key]) + '"'
                else:
                    print('"' + key + '" was skipped as it is not a valid customization for ' + q_type + ' questions')

            question.write('<p><b>' + q_txt[2:q_txt.index('\n')].strip() + '</b></p>\n' +
                           '<p style="margin-left: 15px">' + q_txt[q_txt.index('\n'):] + '</p>\n')

            answer = parsed_q['header'][part_name]['instructor_answers']
            if q_type in SINGLE:
                question.write('<pl-' + q_type + ' answers_name="' + answer + '"' + pl_options + '>\n')
            elif q_type in MULTIPLE:
                question.write('<pl-' + q_type + ' answers_name="' + part_name + '"' + pl_options + '>\n')
                choices = [s.strip() for s in ans_section.split('-')]
                del choices[0]

                if type(answer) != list:
                    answer = [answer]
                for choice in choices:
                    question.write('\t<pl-answer correct="' +
                                   str(any(ans in choice for ans in answer)) + '">' +
                                   choice + '</pl-answer>\n')
            else:  # other element types, such as images, that require their own formatting
                pass
            question.write('</pl-' + q_type + '>\n')

            if i < parsed_q['num_parts']:
                question.write('<hr/>\n')

    # Creating server.py file
    server_info = parsed_q['header']['server']  # isolate server info
    eoi_index = server_info.index('\n', server_info.rindex("import"))
    server_info = server_info[:eoi_index].strip() + "\n\n\ndef generate(data):\n\t" + \
                  server_info[eoi_index:].strip().replace('\n', '\n\t') + "\n"  # add generate method
    with open(out_dir + "/server.py", 'w') as server:
        server.write(server_info)
