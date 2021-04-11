from pathlib import Path
import yaml

# open file
problem_file_name = 'NU_U17-2-03-005.pg'  # short answer
path = '../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/2.Kinematics/' + problem_file_name
file = open(path, 'r')
file_contents = file.read()

# declare variables

metadata = "## "
title_src = "TitleText1"
author_src = "AuthorText1"
editor_src = "Editor"
db_src = "DB"
date_src = "Date"

title = author = editor = date = source = problem_type = outcomes = assets = server = ""
tags = []

# get metadata from file

for item in file_contents.split("\n"):
    if metadata + title_src in item:
        title = item[item.find("(") + 1:item.find(")")].replace("'", "")
    if metadata + author_src in item:
        author = item[item.find("(") + 1:item.find(")")].replace("'", "")
    if metadata + editor_src in item:
        editor = item[item.find("(") + 1:item.find(")")].replace("'", "")
    if metadata + db_src in item:
        tags.append(item[item.find("(") + 1:item.find(")")].replace("'", ""))
    if metadata + date_src in item:
        date = item[item.find("(") + 1:item.find(")")].replace("'", "")


# get problem text from file
problem_text = "Problem Text TBD\n"

# get answer from file
answer_section = "Solution Text TBD"


# Preparing the YAML dictionary

# This solution is copied from this SO answer: https://stackoverflow.com/a/45004775/2217577
yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str


def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)


yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

source = "https://github.com/openwebwork/webwork-open-problem-library"
yaml_dict = {}

yaml_dict['title'] = title
yaml_dict['author'] = author
yaml_dict['date'] = date
yaml_dict['editor'] = editor
yaml_dict['source'] = source
yaml_dict['type'] = problem_type
yaml_dict['tags'] = tags
yaml_dict['outcomes'] = ['TBD']
yaml_dict['assets'] = ['TBD']
# yaml_dict['server'] = full_python #'import random \\n b=u'
# pprint(yaml_dict)
print(yaml.safe_dump(yaml_dict, sort_keys=False))

start = "# {{ vars.title }}\n\n## Question Text\n\n"

Path("test_question.md").write_text('---\n' + \
                                    yaml.safe_dump(yaml_dict, sort_keys=False) + \
                                    '---\n' + \
                                    start + \
                                    problem_text + \
                                    answer_section)
