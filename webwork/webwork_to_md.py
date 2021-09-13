import os
from pathlib import Path
from pprint import pprint
import yaml
import re
import time

# TODO: unify variable names
# TODO: optimize code to run faster
# TODO: modularize code w/ functions and/or separate python files
# TODO: handle exception instead of passing them
# TODO: handle answer section without hint

# loop through every file in the dir
root_path = '../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/12.Fluid_Dynamics_and_Medical_Applications/'
root_dest_folder = 'Output/green/'

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
    question_body = [file_content[file_content.find(problem_body_start_src):file_content.rfind(problem_body_end_src)]]
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
        else:
            editor_ = 'N/A'
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


def determine_problem_type(question_ans, filename):
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

    if not question_type:
        question_type.append("Unknown")

    return {
        'answer_variable': answer_variable,
        'answer_type_raw': answer_type_raw,
        'question_type': question_type,
        'filename': filename}


def yaml_dump(directory_info, metadata, question_format, server, image_dic, question_text, question_units, question_parts):
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
    yaml_dict['source'] = source
    yaml_dict['template_version'] = 1.2
    yaml_dict['editor'] = metadata['editor']
    # yaml_dict['type'] = question_type['question_type']
    yaml_dict['outcomes'] = ['TBD']
    yaml_dict['difficulty'] = ['TBD']
    yaml_dict['randomization'] = ['TBD']
    yaml_dict['taxonomy'] = ['TBD']
    yaml_dict['span'] = ['TBD']
    yaml_dict['length'] = ['TBD']
    yaml_dict['tags'] = metadata['tags']
    yaml_dict['assets'] = image_dic['image_name']
    yaml_dict['server'] = server
    for part_number, part_type in zip(question_parts, question_format):
        yaml_dict['part' + str(part_number+1)] = ''.join(
f"""
type: {part_type}
pl-customizations:
  weight: 1
  hide-answer-panel: true

""").strip('\n')
    question_images = image_dic['image_line_md']
    Path(directory_info['root_dest_folder'] + directory_info['dest_file_path'] + "/" + directory_info['filename'] + ".md").write_text('---\n'
                                                                                + yaml.safe_dump(yaml_dict, sort_keys=False)
                                                                                + '---\n\n'
                                                                                + ''.join(f'\n{image}' for image in question_images)
                                                                                + ''.join(f'## Part {part} \n {question} \n' for part, question in zip(question_parts, question_text))
                                                                                + '\n\n'
                                                                                + '### Answer Section \n'
                                                                                + str(question_units) + '\n\n'
                                                                                + '## pl-submission-panel \n\n\n'
                                                                                + '## pl-answer-panel \n\n\n'
                                                                                + '## Rubric \n\n\n'
                                                                                + '## Solution \n\n\n'
                                                                                + '## Comments \n\n\n')
                                                                                # + ''.join(f'{value}' for key, value in section.items())


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
    hint = ''
    question_units = ''
    question_raw = []
    image_alt_text = []
    question_with_image = ''
    question_no_image = ''
    part_headers = []
    question_part = []

    # split question into sections based on "$PAR"
    for question in question_body:
        if "image(" in question:
            question_with_image = question.split('$PAR\n')
        else:
            question_no_image = question.split('$PAR\n')

    # DEBUGGING:
    # pprint("<---------------- START ---------------->")
    # if len(question_with_image) > 0:
    #     pprint(question_with_image)
    # if len(question_no_image) > 0:
    #     pprint(question_no_image)

    # for each section of the question
    for question_section in question_with_image:
        # if the section is not empty
        if len(question_section) > 0:
            # remote all the \n in the section
            section_clean = question_section.replace('\n', '')
        # if section is NOT the beginning
        #     pprint("<---------------- IN PROGRESS ---------------->")
        #     pprint(section_clean)
            if not section_clean.startswith(problem_body_start_src):
                if section_clean.endswith('</strong>') or section_clean.endswith('</b>'):
                    hint = section_clean
                # if section does NOT include hint
                if hint not in section_clean:
                    subsection = help_problem_extract_ans_units(section_clean)
                    subsection_text = subsection['section']
                    question_units = subsection['final_ans_units']
                    subsection_multi_part = help_problem_extract_ans_type(subsection_text)
                    subsection_multi_part_ans_type = subsection_multi_part['ans_type']
                    subsection_clean = subsection_multi_part['problem_clean']
                    # the remainder of the text contains image alt text and the actual question (contains LaTeX)
                    for image_alt in image_alt_text:
                        # if text does NOT contain image alt text, then the text is the actual question w/ LaTeX
                        if image_alt not in subsection_clean:
                            # append all question sections to variable
                            question_raw = help_problem_extract_append(subsection_clean, question_raw)
                            question_part = append_part_counter(len(question_raw)-1, part_headers)

# for each section of the question
    for question_section in question_no_image:
        # if the section is not empty
        if len(question_section) > 0:
            # remote all the \n in the section
            section_clean = question_section.replace('\n', '')
            # DEBUGGING:
            # pprint("<---------------- IN PROGRESS ---------------->")
            # pprint(section_clean)
            # if section is NOT the beginning i.e. generic text about hint
            if not section_clean.startswith(problem_body_start_src):
                if section_clean.endswith('</strong>') or section_clean.endswith('</b>'):
                    hint = section_clean
                # if section does NOT include hint
                if hint not in section_clean:
                    subsection = help_problem_extract_ans_units(section_clean)
                    subsection_text = subsection['section']
                    question_units = subsection['final_ans_units']
                    subsection_multi_part = help_problem_extract_ans_type(subsection_text)
                    subsection_multi_part_ans_type = subsection_multi_part['ans_type']
                    subsection_clean = subsection_multi_part['problem_clean']
                    question_raw = help_problem_extract_append(subsection_clean, question_raw)
                    question_part = append_part_counter(len(question_raw)-1, part_headers)

# DEBUGGING:
#     pprint("<---------------- DONE ---------------->")
#     pprint(question_raw)
    return {'question_text': question_raw,
            'question_parts': question_part,
            'question_units': question_units}


def append_part_counter(part_counter, part_headers):
    if part_counter not in part_headers:
        part_headers.append(part_counter)
    return part_headers


def extract_problem_type(problem_subsection, filename):
    question_format_raw = re.findall("(ANS\(.+?\);)", str(problem_subsection))
    return determine_problem_type(question_format_raw, filename)


def help_problem_extract_ans_units(problem_subsection):
    final_ans_units = ''
    section_clean = ''
    if not problem_subsection.startswith("\\{ image") and not problem_subsection.endswith(") \\}"):
        # if section is the end i.e. ans_rule (determines the length of the answer)
        if problem_subsection.startswith("\\{ans_rule") and problem_subsection.endswith("\\)"):
            # extract the question units using regex
            final_ans_units = re.findall('textrm{(.+?)}', problem_subsection)
        if not problem_subsection.startswith("\\{ans_rule") and not problem_subsection.endswith("\\)"):
            section_clean = problem_subsection
    return {'section': section_clean,
            'final_ans_units': final_ans_units}


def help_problem_extract_ans_type(problem_subsection):
    ans_type = []
    problem_ans_type_removed = []
    if problem_subsection.startswith("END_TEXT"):
        ans_type = re.search(r"END_TEXT(.*)BEGIN_TEXT", str(problem_subsection))
        problem_ans_type_removed = re.sub(r"END_TEXT(.*)BEGIN_TEXT", "", str(problem_subsection))
    else:
        problem_ans_type_removed = problem_subsection

    return {'ans_type': ans_type,
            'problem_clean': problem_ans_type_removed}


def help_problem_extract_append(problem_subsection, final_dic):
    if len(problem_subsection) > 1:
        problem_stripped = problem_subsection.replace('\\', '').replace('textrm', '').replace('{', '').replace('}', '')\
            .replace('&middot;', '$\\cdot$').replace('END_TEXT', '').replace('BEGIN_TEXT', '').strip()
        if re.match(r'.\) ', problem_stripped):
            subsection_without_part_num = problem_stripped[3:]
            final_dic.append(subsection_without_part_num)
        else:
            final_dic.append(problem_stripped)

    return final_dic


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
                    filename = file[0:file.find('.')]
                    question_file = open(source_filepath, 'r')
                    file_contents = question_file.read()
                    dest_file_path = root.removeprefix(root_path)

                    split_file(file_contents)
                    file_contents_dic = split_file(file_contents)
                    metadata_dic = metadata_extract(file_contents_dic['metadata'])
                    dir_info = {
                        'filename': filename,
                        'file_dir': file_dir,
                        'root_dest_folder': root_dest_folder,
                        'dest_file_path': dest_file_path
                    }
                    question_body = file_contents_dic['question_body']
                    image_dic = image_extract(question_body)
                    question_extract = problem_extract(question_body)
                    question_text = question_extract['question_text']
                    question_parts = question_extract['question_parts']
                    question_units = question_extract['question_units']
                    question_formats = extract_problem_type(file_contents, dir_info['filename'])['question_type']

                    yaml_dump(dir_info, metadata_dic, question_formats, server, image_dic, question_text,
                              question_units, question_parts)
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
