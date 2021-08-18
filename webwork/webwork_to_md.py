import os
from pathlib import Path
from pprint import pprint
import yaml
import re
from string import ascii_lowercase
import time

# TODO: unify variable names
# TODO: optimize code to run faster
# TODO: modularize code w/ functions and/or separate python files
# TODO: handle exception instead of passing them
# TODO: handle answer section without hint

# loop through every file in the dir
root_path = '../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/2.Kinematics'
root_dest_folder = 'Output/hello'

# variable declaration
counter = 0
output = []
source_files = []
src_dirs = []
title = topic = author = editor = date = source = template_version = problem_type = attribution = outcomes = difficulty = randomization = taxonomy = ""
tags = assets = altText = image_line = []
total_start_time = time.process_time()

# server variables
server_imports = """
imports: |
  import random
  import problem_bank_helpers as pbh
""".strip('\n')
server_generate_names = "TBD"
server_generate_phrases = "TBD"
server_generate_random_var = "TBD"
server_generate_dic = "TBD"
server_generate_answers = "TBD"
server_generate = f"""
generate: |
    data2 = pbh.create_data2()

    # define or load names/items/objects from server files
    {server_generate_names}
    # store phrases etc
    {server_generate_phrases}
    # Randomize Variables
    {server_generate_random_var}
    # store the variables in the dictionary "params"
    {server_generate_dic}
    # define possible answers
    {server_generate_answers}
    # Update the data object with a new dict
    data.update(data2)
"""
server_prepare = """
prepare: |
    pass
""".strip('\n')
server_parse = """
parse: |
    pass
"""
server_grade = """
grade: |
    pass
""".strip('\n')
server = f"""{server_imports}{server_generate}{server_prepare}{server_parse}{server_grade}""".strip('\n')

# Variable declaration for Webwork keywords
metadata_end_src = "DOCUMENT();"
marcos_end_src = "TEXT(beginproblem());"
variables_start_src = "showHint"
problem_body_start_src = "BEGIN_TEXT"
problem_body_end_src = "END_TEXT"
hint_start_src = "BEGIN_HINT"
hint_end_src = "END_HINT"
ans_rule_src = "ans_rule"
ans_src = "ANS"
hint_src = "hint"
image_src = "image"

# extract file structure from source directory (handles ALL sub-directories)
# for loop runs based # of folders in src
for root, dirs, files in os.walk(root_path):
    for name in dirs:
        dest_folder = os.path.join(root, name).removeprefix(root_path)
        src_dirs.append(root_dest_folder + dest_folder)


def split_file(file_content):
    # TODO: once all functions are completed, convert global variables above into local variables
    # split the file into bite-size pieces to increase speed and reduce bugs
    metadata_content = file_content[:file_content.find(metadata_end_src)]
    macros = file_content[file_content.find(metadata_end_src):file_content.find(marcos_end_src)]
    question_variables = file_content[file_content.find(marcos_end_src):file_content.find(problem_body_start_src)]
    question_body = [file_content[file_content.find(problem_body_start_src):file_content.find(problem_body_end_src)]]
    question_ans = re.findall(r"ANS(\(.+?[?<!)]\));", file_content)
    question_hint = [file_content[file_content.find(hint_start_src):file_content.find(hint_end_src)]]
    return {'metadata': metadata_content,
            'macros': macros,
            'question_variables': question_variables,
            'question_body': question_body,
            'question_ans': question_ans,
            'question_hint': question_hint}


def metadata_extract(metadata_content):
    metadata = "## "
    chapter_src = "DBchapter"
    section_src = "DBsection"
    author_src = "AuthorText1"
    editor_src = "Editor"
    keywords_src = "KEYWORDS"
    date_src = "Date"

    title_ = topic_ = author_ = editor_ = tags_ = date_ = None

    # Look for keywords declared above and extract them from metadata content
    for item in metadata_content.split("\n"):
        if metadata + chapter_src in item:
            title_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
        if metadata + section_src in item:
            topic_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
        if metadata + author_src in item:
            author_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
        if metadata + editor_src in item:
            editor_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
        if keywords_src in item:
            tags_ = item[item.find("(") + 1:item.find(")")].replace("'", "").replace(",", "").split()
        if metadata + date_src in item:
            date_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
    return {'title': title_,
            'topic': topic_,
            'author': author_,
            'editor': editor_,
            'tags': tags_,
            'date': date_}


def determine_problem_type(question_ans):
    # determine what type of question is based on the ANS(type)
    numerical_type = "num_cmp"
    functional_type = "fun_cmp"
    checkbox_type = "checkbox_cmp"
    text_type = "str_cmp"
    question_type = []

    # extracts answer variable from ANS(num_cmp("variable"))
    answer_variable = re.findall(r'"\$([^"]*)"', str(question_ans))
    # extracts problem type from ANS i.e num_cmp, fun_cmp etc.
    answer_type_raw = re.findall(r'\((.*?)\(', str(question_ans))

    # determine answer type based on the raw answer from question
    for answer_type in answer_type_raw:
        if numerical_type in answer_type:
            question_type.append("Numerical")
        elif functional_type in answer_type:
            question_type.append("Functional")
        elif checkbox_type in answer_type:
            question_type.append("Checkbox")
        elif text_type in answer_type:
            question_type.append("Text")
        else:
            question_type.append("Unknown")
    return {
        'answer_variable': answer_variable,
        'answer_type_raw': answer_type_raw,
        'question_type': question_type}


def yaml_dump(directory_info, metadata, question_type, server, section, image_dic):
    # This solution is copied from this SO answer: https://stackoverflow.com/a/45004775/2217577
    yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

    def repr_str(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
        return dumper.org_represent_str(data)

    yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

    source = f"https://github.com/open-resources/webwork-open-problem-library/tree/master/{directory_info['file_dir']}"
    yaml_dict = {}

    # populate yaml_dic with values from args
    yaml_dict['title'] = metadata['title']
    yaml_dict['topic'] = metadata['topic']
    yaml_dict['author'] = metadata['author']
    yaml_dict['date'] = metadata['date']
    yaml_dict['editor'] = metadata['editor']
    yaml_dict['tags'] = metadata['tags']
    yaml_dict['source'] = source
    yaml_dict['template_version'] = 1.1
    # yaml_dict['type'] = question_type['question_type']
    yaml_dict['difficulty'] = ['TBD']
    yaml_dict['randomization'] = ['TBD']
    yaml_dict['taxonomy'] = ['TBD']
    yaml_dict['outcomes'] = ['TBD']
    yaml_dict['assets'] = image_dic['image_name']
    yaml_dict['server'] = server
    # iterate through # of sections and print question type based on each section
    try:
        # TODO: revisit this section
        for part_counter in range(0, len(section)):
            # print(part_counter)
            yaml_dict['part' + str(part_counter + 1 if part_counter < 2 else part_counter)] = ''.join(f"""
type:
    {question_type[part_counter]}
pl-customizations:
    weight: 1
""").strip('\n')
    except Exception as e:
        pass
        # create a new .md file using the file path and filename, write data into it
        Path(directory_info['root_dest_folder'] + directory_info['dest_file_path'] + "/" + directory_info['filename'] + ".md").write_text('---\n'
                                                                                + yaml.safe_dump(yaml_dict, sort_keys=False)
                                                                                + '---\n\n'
                                                                                + '## Question Section '
                                                                                + '\n\n'
                                                                                + ''.join(f'\n{image}' for image in image_dic['image_line_md'])
                                                                                + '\n\n')
                                                                                # + problem_text
                                                                                # + '\n\n'
                                                                                # + ''.join(f'{value}' for key, value in section.items())
                                                                                # + '\n\n'
                                                                                # + '## Answer Section'
                                                                                # + '\n\n'
                                                                                # + answer_section)


def image_extract(question_content):
    image_src = "image("
    image_line = []
    image_alt_text = []
    image_name = []

    # iterate through each question part in the questions
    for question_part in question_content:
        # determine if the question contains an image
        if image_src in question_part:
            # extract image name and alt text using regex
            image_name = re.findall(' "(.+?)"', str(question_content).strip())
            image_alt_text = re.findall('="(.+?)"', str(question_content).strip())

    # bundle up the image name and alt text to create a .md image line
    for image_alt, image_filename in zip(image_alt_text, image_name):
        if image_alt:
            image_line.append('![' + image_alt.strip() + '](' + image_filename + ')')
        else:
            image_line.append('![](' + image_filename + ')')

    return {'image_name': image_name,
            'image_alt': image_alt_text,
            'image_line_md': image_line}


def problem_extract(question_body):
    question_units = ''
    question_raw = []
    image_alt_text = []
    pprint(question_body)

    # split question into sections based on "$PAR"
    for question in question_body:
        question_split = question.split('$PAR\n')

    # for each section of the question
    for question_section in question_split:
        # if the section is not empty
        if len(question_section) > 0:
            # remote all the \n in the section
            section_clean = question_section.replace('\n', '')
            # if section is NOT the beginning i.e. generic text about hint
            if not section_clean.startswith(problem_body_start_src) and not section_clean.endswith('</strong>'):
                # if section contains information about image i.e. image name and tag
                if section_clean.startswith("\\{ image") and section_clean.endswith(") \\}"):
                    # determine the alt text of the question (to be used later)
                    image_alt_text = re.findall('="(.+?)"', section_clean.strip())

                #  the remainder of the text contains ans_rule, image alt tag and actual question
                else:
                    # if section is the end i.e. ans_rule (determines the length of the answer)
                    if section_clean.startswith("\\{ans_rule") and section_clean.endswith("\\)"):
                        # extract the question units using regex
                        question_units = re.findall('textrm{(.+?)}', section_clean)

                    # the remainder of the text contains image alt text and the actual question (contains LaTeX)
                    else:
                        # iterate through the image alt tag
                        for image_alt in image_alt_text:
                            # if text does NOT contain image alt text, then the text is the actual question w/ LaTeX
                            if image_alt not in section_clean:
                                # append all question sections to variable
                                question_raw.append(section_clean)
    return {'question_raw': question_raw}

# for loop runs based # of folders in src
for root, dirs, files in os.walk(root_path):
    # create dest file structure based on source directory
    for dir_path in src_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    # iterate through each file
    for file in files:
        if file.endswith('.pg'):
            file_start_time = time.process_time()
            source_files.append(os.path.join(root, file))
            for source_filepath in source_files:
                try:
                    file_dir = source_filepath[source_filepath.find("Contrib"):]
                    filename = file[1:file.find('.')]
                    question_file = open(source_filepath, 'r')
                    file_contents = question_file.read()
                    dest_file_path = root.removeprefix(root_path)

                    split_file(file_contents)
                    file_contents_dic = split_file(file_contents)
                    # pprint(file_contents_dic['question_ans'])
                    metadata_dic = metadata_extract(file_contents_dic['metadata'])
                    question_type = determine_problem_type(file_contents_dic['question_ans'])
                    dir_info = {
                        'filename': filename,
                        'file_dir': file_dir,
                        'root_dest_folder': root_dest_folder,
                        'dest_file_path': dest_file_path
                    }
                    question_body = file_contents_dic['question_body']
                    image_dic = image_extract(question_body)
                    question_text = problem_extract(question_body)

                    # ------------------------ Preparing Problem Text ------------------------ #

                    if hint_start_src in file_contents:
                        problem_full = file_contents[
                                       file_contents.index(problem_body_start_src):file_contents.index(hint_start_src)]
                    else:
                        problem_full = file_contents[
                                       file_contents.index(problem_body_start_src):file_contents.index(
                                           problem_body_end_src)]
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
                        .replace('BR', '') \
                        .replace('textrm', '') \
                        .strip()

                    # find all problem text between
                    problem_multi_para = problem_header.replace(problem_body_end_src, "").replace(problem_body_start_src,
                                                                                                "")

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
                        if parts_dirty[alphabet]:
                            section_header = parts_dirty[alphabet].group()[0].capitalize()
                            parts_clean[alphabet] = re.sub(rf"{alphabet}\) ", "", parts_dirty[alphabet].group())
                            section[alphabet] = "## " + section_header + "\n" \
                                                + parts_clean[alphabet] + "\n" \
                                                + "### Answer Section" + "\n"

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
                            answer_section = "from random import randrange\n" + answer_section.replace('random',
                                                                                                       'randrange')
                    else:
                        # TODO: handle answer section without hint
                        answer_section = ""

                    yaml_dump(dir_info, metadata_dic, question_type, server, section, image_dic)
                    end_file_time = time.process_time()
                    file_process_time = end_file_time - file_start_time
                    counterString = '#' + str(counter + 1) + ' - [' + str(round(file_process_time, 5)) + '] '
                    currentFile = root_dest_folder + dest_file_path + "/" + filename

                    if currentFile not in output:
                        counter = counter + 1
                        print(counterString + currentFile)
                        output.append(currentFile)

                except Exception as e:
                    print(e)
                    pass

# ------------------------ STATS ------------------------ #
total_end_time = time.process_time()
process_time_seconds = total_end_time - total_start_time
print('total time:', round(process_time_seconds / 60, 2), 'minutes,', round(process_time_seconds, 2), 'seconds')
print('avg time per each file:', round(process_time_seconds / counter, 2), 'seconds [', counter, '] files')
