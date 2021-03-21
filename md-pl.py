import uuid
import re

with open("stem.md", 'r') as infile:
    raw = infile.read()

metadata = re.search("### metadata(.*?)###", raw, flags=re.DOTALL).group(1)
question_txt = re.search("### question(.*?)###", raw, flags=re.DOTALL).group(1)
parameters = re.search("### parameters(.*?)###", raw, flags=re.DOTALL).group(1)
solution = re.search("### solution(.*?)###", raw, flags=re.DOTALL).group(1)

title = re.search("title:(.*)", metadata).group(1).strip()
topic = re.search("topic:(.*)", metadata).group(1).strip()
tags = re.search("tags:(.*)", metadata).group(1).strip().split(',')
q_type = re.search("q_type:(.*)", metadata).group(1).strip()
params = parameters.splitlines()

if q_type == 'numeric':
    sig_figs = re.search("sig_figs:(.*)", metadata).group(1).strip()
    ans_name = re.search("(.*?)=", solution).group(1).strip()
elif q_type == 'mc':
    ans_choices = solution.strip().splitlines()


def html_ans(qtype):
    ans_string = ''
    if qtype == 'numeric':
        ans_string = """<pl-number-input answers-name=\"""" + ans_name + """\" comparison="sigfig" digits=\"""" \
                     + str(sig_figs) + """\" label="$""" + ans_name + """=$"></pl-number-input>""",
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
                     + ans_name + "\n",

    elif q_type == 'mc':
        choice_name = '`'
        for choice in ans_choices:
            choice_name = chr(ord(choice_name) + 1)
            ans_string += "\n    data['correct_answers']['" + choice_name + "'] = " + choice.strip()[1:].replace('**',
                                                                                                                 '')
    return ans_string


with open("info.json", 'w', newline='') as info:
    info.write("""{
        "uuid": \"""" + str(uuid.uuid4()) + """\",
        "title": \"""" + title + """",
        "topic": \"""" + topic + """",
        "tags":  """ + str(tags).replace("\'", "\"") + """,
        "type": "v3"
    }""")

with open("server.py", 'w', newline='') as server:
    server.write("import random\n\n\n")
    server.write("def generate(data):\n")
    for param in params:
        if "=" in param:
            server.write("    " + param.strip() + "\n")
            var_name = re.search("(.*?)=", param).group(1).strip()
            question_txt = question_txt.replace("[" + var_name + "]", "{{params." + var_name + "}}")
            server.write("    data['params']['" + var_name + "'] = " + var_name + "\n")
    server.write(server_ans(q_type))

with open("question.html", 'w', newline='') as question:
    question.write("""<pl-question-panel>
    <p>""" + question_txt.strip() + """</p>
</pl-question-panel>""")
    question.write(html_ans(q_type))
