import ctypes
import uuid
import re
import os

current_dir = os.path.dirname(__file__)
source_dir = current_dir + "/md_files"
try:
    os.mkdir(source_dir)
    ctypes.windll.user32.MessageBoxW(0, u"Place question files in md_files folder ", u"Markdown_to_PL.py", 0)
    quit()
except FileExistsError:
    pass

# -----Process questions (loop)
_, _, filenames = next(os.walk(source_dir))
if not filenames:
    ctypes.windll.user32.MessageBoxW(0, u"No questions in source folder", u"Markdown_to_PL.py", 0)
for question_stem in filenames:
    with open(source_dir + "/" + question_stem, 'r') as infile:
        raw = infile.read()

    try:
        metadata = re.search("### metadata(.*?)###", raw, flags=re.DOTALL).group(1)
    except AttributeError:
        ctypes.windll.user32.MessageBoxW(0, u"Missing metadata", u"Markdown_to_PL.py", 0)
        quit()
    try:
        question_txt = re.search("### question(.*?)###", raw, flags=re.DOTALL).group(1)
    except AttributeError:
        ctypes.windll.user32.MessageBoxW(0, u"Missing question text", u"Markdown_to_PL.py", 0)
        quit()
    try:
        parameters = re.search("### parameters(.*?)###", raw, flags=re.DOTALL).group(1)
    except AttributeError:
        ctypes.windll.user32.MessageBoxW(0, u"Missing parameters", u"Markdown_to_PL.py", 0)
        quit()
    try:
        solution = re.search("### solution(.*?)###", raw, flags=re.DOTALL).group(1)
    except AttributeError:
        ctypes.windll.user32.MessageBoxW(0, u"Missing solution", u"Markdown_to_PL.py", 0)
        quit()

    title = re.search("title:(.*)", metadata).group(1).strip()
    topic = re.search("topic:(.*)", metadata).group(1).strip()
    tags = re.search("tags:(.*)", metadata).group(1).strip().split(',')
    q_type = re.search("q_type:(.*)", metadata).group(1).strip()
    params = parameters.splitlines()

    try:
        os.mkdir(current_dir + "/converted_q's")
    except FileExistsError:
        pass

    output_dir = current_dir + "/converted_q's/" + title
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    if q_type == 'numeric':
        sig_figs = re.search("sig_figs:(.*)", metadata).group(1).strip()
        ans_name = re.search("(.*?)=", solution).group(1).strip()
    elif q_type == 'mc':
        ans_choices = solution.strip().splitlines()


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
            ans_string = "    " + solution.strip() + "\n    data['correct_answers']['" + ans_name + "'] = " \
                         + ans_name + "\n"
        elif q_type == 'mc':
            choice_name = '`'
            for choice in ans_choices:
                choice_name = chr(ord(choice_name) + 1)
                ans_string += "\n    data['correct_answers']['" + choice_name + "'] = " \
                              + choice.strip()[1:].replace('**', '')
        return ans_string


    # ------ Writing to files
    with open(output_dir + "/info.json", 'w', newline='') as info:
        info.write("""{
            "uuid": \"""" + str(uuid.uuid4()) + """\",
            "title": \"""" + title + """",
            "topic": \"""" + topic + """",
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
                question_txt = question_txt.replace("[" + var_name + "]", "{{params." + var_name + "}}")
                server.write("    data['params']['" + var_name + "'] = " + var_name + "\n")
        server.write(server_ans(q_type))

    with open(output_dir + "/question.html", 'w', newline='') as question:
        question.write("""<pl-question-panel>
        <p>""" + question_txt.strip() + """</p>
    </pl-question-panel>""")
        question.write(html_ans(q_type))
