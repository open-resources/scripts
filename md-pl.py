import uuid
import re
import os

current_dir = os.path.dirname(__file__)
source_dir = current_dir + "/md_files"
try:
    os.mkdir(source_dir)
    input("------------------------------------------\n"
          "Place question files in 'md_files' folder.\n"
          "Press enter to continue\n"
          "------------------------------------------")
except FileExistsError:
    pass

# -----Process questions
_, _, filenames = next(os.walk(source_dir))
if not filenames:
    input("----------------------------\n"
          "Question source folder empty\n"
          "----------------------------")

# Loop start
for question_stem in filenames:
    with open(source_dir + "/" + question_stem, 'r') as infile:
        raw = infile.read()


    def section_content(section_name):
        regex = "### " + section_name + "(.*?)###"
        return re.search(regex, raw, flags=re.DOTALL).group(1).strip()


    sections = ['metadata', 'question', 'parameters', 'solution']
    section_body = {}
    try:
        for section in sections:
            section_body[section] = section_content(section)
    except AttributeError:
        print(question_stem + " is missing its " + section + " section!")
        continue


    def find_tag(tag_name):
        regex = tag_name + ":(.*)"
        return re.search(regex, section_body['metadata']).group(1).strip()


    tags = ['title', 'topic', 'tags', 'q_type']
    tag_contents = {}
    try:
        for tag in tags:
            tag_contents[tag] = find_tag(tag)
    except AttributeError:
        print(question_stem + " needs a " + tag)
        continue

    params = section_body['parameters'].splitlines()

    try:
        os.mkdir(current_dir + "/converted_q's")
    except FileExistsError:
        pass

    output_dir = current_dir + "/converted_q's/" + tag_contents['title']
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    if tag_contents['q_type'] == 'numeric':
        sig_figs = re.search("sig_figs:(.*)", section_body['metadata']).group(1).strip()
        ans_name = re.search("(.*?)=", section_body['solution']).group(1).strip()
    elif tag_contents['q_type'] == 'mc':
        ans_choices = section_body['solution'].splitlines()


    def html_ans(qtype):
        ans_string = ''
        if qtype == 'numeric':
            ans_string = """<pl-number-input answers-name=\"""" + ans_name + """\" comparison="sigfig" digits=\"""" \
                         + str(sig_figs) + """\" label="$""" + ans_name + """=$"></pl-number-input>"""
        elif qtype == 'mc':
            ans_string = """<pl-multiple-choice answers-name="acc" weight="1">"""

            choice_name = '`'
            for choice in ans_choices:
                choice_name = chr(ord(choice_name) + 1)
                ans_string += "\n<pl-answer correct=\"" + str(choice != choice.replace('**', '')) + \
                              "\">{{correct_answers." + choice_name + "}}</pl-answer>"
            ans_string += "\n</pl-multiple-choice>"
        return ans_string


    def server_ans(qtype):
        ans_string = ''
        if qtype == 'numeric':
            ans_string = "    " + section_body[
                'solution'].strip() + "\n    data['correct_answers']['" + ans_name + "'] = " \
                         + ans_name + "\n"
        elif tag_contents['q_type'] == 'mc':
            choice_name = '`'
            for choice in ans_choices:
                choice_name = chr(ord(choice_name) + 1)
                ans_string += "\n    data['correct_answers']['" + choice_name + "'] = " \
                              + choice.strip()[2:].replace('**', '')
            ans_string += '\n'
        return ans_string


    # ------ Writing to files
    with open(output_dir + "/info.json", 'w', newline='') as info:
        info.write("""{
            "uuid": \"""" + str(uuid.uuid4()) + """\",
            "title": \"""" + tag_contents['title'] + """",
            "topic": \"""" + tag_contents['topic'] + """",
            "tags":  """ + str(tags).replace("\'", "\"") + """,
            "type": "v3"
        }""")

    with open(output_dir + "/server.py", 'w', newline='') as server:
        server.write("import random\n\n\n")
        server.write("def generate(data):\n")
        for param in params:
            if "=" in param:
                server.write("    " + param.strip() + "\n")
                var_name = re.search("(.*?)=", param).group(1).strip()
                section_body['question'] = section_body['question'].replace("[" + var_name + "]",
                                                                            "{{params." + var_name + "}}")
                server.write("    data['params']['" + var_name + "'] = " + var_name + "\n")
        server.write(server_ans(tag_contents['q_type']))

    with open(output_dir + "/question.html", 'w', newline='') as question:
        question.write("""<pl-question-panel>
        <p>""" + section_body['question'] + """</p>
    </pl-question-panel>""")
        question.write(html_ans(tag_contents['q_type']))

input('Press Enter to finish')
