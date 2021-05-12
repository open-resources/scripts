import os
from pathlib import Path
import yaml
import re

# open single file
# problem_file_name = 'NU_U17-2-07-010'
# path = '../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/2.Kinematics/' + problem_file_name + '.pg'
# file = open(path, 'r')
# file_contents = file.read()

# loop through every file in the dir
file_path = '../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/2.Kinematics/'
counter = 0
for root, dir, files in os.walk(file_path):
    for file in files:
        if file.endswith('.pg'):
            filename = file[1:file.find('.')]
            counter = counter + 1
            print(filename + ' - ' + str(counter))

            question_file = open(file_path + file, 'r')
            file_contents = question_file.read()

            # declare variables
            metadata = "## "
            chapter_src = "DBchapter"
            section_src = "DBsection"
            author_src = "AuthorText1"
            editor_src = "Editor"
            keywords_src = "KEYWORDS"
            date_src = "Date"

            title = author = editor = date = source = problem_type = outcomes = assets = server = ""
            tags = []

            # get metadata from file
            for item in file_contents.split("\n"):
                if metadata + chapter_src in item:
                    title = item[item.find("(") + 1:item.find(")")].replace("'", "")
                if metadata + section_src in item:
                    title += " - " + item[item.find("(") + 1:item.find(")")].replace("'", "")
                if metadata + author_src in item:
                    author = item[item.find("(") + 1:item.find(")")].replace("'", "")
                if metadata + editor_src in item:
                    editor = item[item.find("(") + 1:item.find(")")].replace("'", "")
                if keywords_src in item:
                    tags = item[item.find("(") + 1:item.find(")")].replace("'", "").replace(",", "").split()
                if metadata + date_src in item:
                    date = item[item.find("(") + 1:item.find(")")].replace("'", "")

            # get problem text from file
            start_of_problem_src = "BEGIN_TEXT"
            end_of_problem_src = "END_TEXT"
            begin_hint_src = "BEGIN_HINT"

            problem_full = file_contents[file_contents.index(start_of_problem_src):file_contents.index(begin_hint_src)]
            problem_header = problem_full \
                .replace(' \\', '') \
                .replace('\\', '') \
                .replace('/', '') \
                .replace('<strong>', '') \
                .replace('$', '') \
                .replace('{', '') \
                .replace('}', '') \
                .replace('PAR', '') \
                .replace('textrm', '') \
                .strip()
            # find all problem text between
            problem_multi_para = problem_header.replace(end_of_problem_src, "").replace(start_of_problem_src, "")

            # remove ans_rule line from problem
            problem_clean_up = re.sub(r"ans_rule(.+?[(])(.+?[)])", '', problem_multi_para)
            # remove ANS line from problem
            problem_no_ans = re.sub(r"ANS(\(.+?[?<!)]\));", '', problem_clean_up)
            # remove empty lines from problem
            problem_no_empty_lines = os.linesep.join([s for s in problem_no_ans.splitlines() if s])
            # remove hint lin from beginning of problem
            problem_text = problem_no_empty_lines[problem_no_empty_lines.index("hint.")+6:]

            # get answer from file
            start_of_answer_src = "showHint"
            end_of_answer_src = "BEGIN_TEXT"

            answer_with_hint = file_contents[file_contents.index(start_of_answer_src):file_contents.index(end_of_answer_src)]
            answer_section = re.sub(rf"{start_of_answer_src} =\d+;", '', answer_with_hint)\
                .replace(end_of_answer_src, '')\
                .replace(';', '')\
                .replace('$', '').strip()
            if "random" in answer_section:
                answer_section = "from random import randrange\n" + answer_section.replace('random', 'randrange')

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

            # print(yaml.safe_dump(yaml_dict, sort_keys=False))
            # print(answer_section)
            # print(problem_text)

            start = "# {{ vars.title }}\n\n## Question Text\n\n"

            Path("Kinematics/" + filename + ".md").write_text('---\n' + \
                                                yaml.safe_dump(yaml_dict, sort_keys=False) + \
                                                '---\n' + \
                                                start + \
                                                problem_text + \
                                                '\n' + \
                                                answer_section)
