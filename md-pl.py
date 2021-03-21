import uuid
import re
import os

with open("stem.md", 'r') as infile:
    raw = infile.read()

metadata = re.search("### metadata(.*?)###", raw, flags=re.DOTALL).group(1)
question_txt = re.search("### question(.*?)###", raw, flags=re.DOTALL).group(1)
parameters = re.search("### parameters(.*?)###", raw, flags=re.DOTALL).group(1)
solution = re.search("### solution(.*?)###", raw, flags=re.DOTALL).group(1)

title = re.search("title:(.*)", metadata).group(1).strip()
topic = re.search("topic:(.*)", metadata).group(1).strip()
tags = re.search("tags:(.*)", metadata).group(1).strip().split(',')
sig_figs = re.search("sig_figs:(.*)", metadata).group(1).strip()

params = parameters.splitlines()
ans_name = re.search("(.*?)=", solution).group(1).strip()

q_type = {
    'numeric': """<pl-number-input answers-name=\"""" + ans_name + """\" comparison="sigfig" digits=\"""" +
               str(sig_figs) + """\" label="$""" + ans_name + """=$"></pl-number-input>""",
    'multiple_choice': "",
    't/f': ""}

with open("info.json", 'w', newline='') as info:
    info.write("""{
        "uuid": \"""" + str(uuid.uuid4()) + """\",
        "title": \"""" + title + """",
        "topic": \"""" + topic + """",
        "tags":  """ + str(tags).replace("\'", "\"") + """,
        "type": "v3"
    }""")

with open("server.py", 'w', newline='') as server:
    server.write("import random\n\n\ndef generate(data):\n")
    for param in params:
        if "=" in param:
            server.write("    " + param.strip() + "\n")
            var_name = re.search("(.*?)=", param).group(1).strip()
            question_txt = question_txt.replace("[" + var_name + "]",
                                                "$" + var_name + " = {{params." + var_name + "}}$")
            server.write("    data['params']['" + var_name + "'] = " + var_name + "\n")
    server.write("    " + solution.strip() + "\n")
    server.write("    data['correct_answers']['" + ans_name + "'] = " + ans_name + "\n")

with open("question.html", 'w', newline='') as question:
    question.write("""<pl-question-panel>
    <p>""" + question_txt.strip() + """</p>
</pl-question-panel>""")
    question.write(q_type.get('numeric'))
