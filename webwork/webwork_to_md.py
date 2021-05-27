import os
from pathlib import Path
import yaml
import re
from string import ascii_lowercase

# loop through every file in the dir
# TODO: change this file path to get files directly from github to ensure they're up-to-date
file_path = '../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/2.Kinematics/'
# file_path = '../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/3.Two_Dimensional_Kinematics/Projectile_Motion/'

# TODO: remove file path for math problems before merging PR ->
# file_path = '../../webwork-open-problem-library/OpenProblemLibrary/FortLewis/Calc3/12-1-Two-variable-functions/'
counter = 0
for root, dir, files in os.walk(file_path):
    for file in files:
        if file.endswith('.pg'):
            filename = file[1:file.find('.')]
            counter = counter + 1

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

            title = author = editor = date = source = problem_type = outcomes = server = ""
            tags = assets = []

            # ------------------------ Preparing Metadata ------------------------ #
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

            # ------------------------ Preparing Problem Text ------------------------ #
            start_of_problem_src = "BEGIN_TEXT"
            end_of_problem_src = "END_TEXT"
            begin_hint_src = "BEGIN_HINT"
            ans_rule_src = "ans_rule"
            ans_src = "ANS"
            hint_src = "hint"
            image_src = "image"

            if begin_hint_src in file_contents:
                problem_full = file_contents[
                               file_contents.index(start_of_problem_src):file_contents.index(begin_hint_src)]
            else:
                problem_full = file_contents[
                               file_contents.index(start_of_problem_src):file_contents.index(end_of_problem_src)]
            # print(file_contents)
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

            # TODO: Clean up and optimize the if / else statements

            # extract image file names from question and save in assets
            if image_src in problem_multi_para:
                num_images = problem_multi_para.count("image")
                for image_src in problem_multi_para:
                    image_file = re.findall(' ".+?"', problem_multi_para.strip())
                    assets = [img.replace('"', '').strip() for img in image_file]
            else:
                assets = ''

            # remove ans_rule line from problem
            if ans_rule_src in problem_multi_para:
                problem_clean_up = re.sub(r"ans_rule(.+?[(])(.+?[)])", '', problem_multi_para)
            else:
                problem_clean_up = ''

            # remove ANS line from problem
            if ans_src in problem_multi_para:
                problem_no_ans = re.sub(r"ANS(\(.+?[?<!)]\));", '', problem_clean_up)
                # remove empty lines from problem
                problem_no_empty_lines = os.linesep.join([s for s in problem_no_ans.splitlines() if s])
            else:
                # remove empty lines from problem
                problem_no_empty_lines = os.linesep.join([s for s in problem_multi_para.splitlines() if s])

            # remove hint lin from beginning of problem
            if hint_src in problem_multi_para:
                problem_no_hint = re.sub(r".*hint.", "", problem_no_empty_lines).strip()
            else:
                problem_no_hint = problem_no_empty_lines

            # Remove image section from problem text
            if "image" in problem_no_hint:
                # Remove image - height
                image_line_1 = re.sub(r"image\( .+", "", problem_no_hint).strip()
                # Remove tex - *
                image_line_2 = re.sub(r"tex.+", "", image_line_1).strip()
                # Remove Figure *
                # TODO: can not remove all "figures" since some questions use the word "figure" in the actual question
                # image_line_3 = re.sub(r"Figure.+", "", image_line_2).strip()
                problem_text = image_line_2
            else:
                problem_text = problem_no_hint

            parts_dirty = parts_clean = {}
            section = {}
            # find multi-part questions and separate each section
            for alphabet in ascii_lowercase[:11]:
                parts_dirty[alphabet] = re.search(rf"{alphabet}\) .*", problem_text)
                # problem_text = re.sub(rf"{alphabet}\) .*", '', problem_text)
                if parts_dirty[alphabet]:
                    section_header = parts_dirty[alphabet].group()[0].capitalize()
                    parts_clean[alphabet] = re.sub(rf"{alphabet}\) ", "", parts_dirty[alphabet].group())
                    section[alphabet] = "## " + section_header + "\n" \
                                        + parts_clean[alphabet] + "\n" \
                                        + "### Answer Section" + "\n"
                    print(filename + " " + section[alphabet])

            # ------------------------ Preparing Answer Section ------------------------ #
            start_of_answer_src = "showHint"
            end_of_answer_src = "BEGIN_TEXT"
            context_src = "Context"

            if start_of_answer_src in file_contents:
                answer_with_hint = file_contents[file_contents.index(start_of_answer_src)
                                                 :file_contents.index(end_of_answer_src)]
                # Remove "Context" from end of file
                if context_src in answer_with_hint:
                    answer_no_context = re.sub(rf"{context_src}.+", "", answer_with_hint)
                else:
                    answer_no_context = answer_with_hint
                answer_section = re.sub(rf"{start_of_answer_src} =\d+;", '', answer_no_context) \
                    .replace(end_of_answer_src, '') \
                    .replace(';', '') \
                    .replace('$', '').strip()
                if "random" in answer_section:
                    answer_section = "from random import randrange\n" + answer_section.replace('random', 'randrange')
            else:
                # TODO: handle answer section without hint
                answer_section = ""

            # ------------------------ Preparing the YAML dictionary ------------------------ #
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
            yaml_dict['assets'] = assets
            # yaml_dict['server'] = full_python #'import random \\n b=u'

            if not assets:
                print('#' + str(counter) + ' - ' + filename)
            else:
                print('#' + str(counter) + ' - ' + filename + "'s Assets: " + str(assets))
            # print(yaml.safe_dump(yaml_dict, sort_keys=False))
            # print(answer_section)
            # print(problem_text)

            Path("Kinematics/" + filename + ".md").write_text('---\n'
                                                              + yaml.safe_dump(yaml_dict, sort_keys=False)
                                                              + '---\n\n'
                                                              + '## Question Section '
                                                              + '\n\n'
                                                              + problem_text
                                                              + '\n'
                                                              + ''.join(f'{value}' for key, value in section.items())
                                                              + '\n\n'
                                                              + '## Answer Section'
                                                              + '\n\n'
                                                              + answer_section)
