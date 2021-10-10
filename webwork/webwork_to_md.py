import os
from pathlib import Path
from pprint import pprint
import yaml
import re
import time
from shutil import copy2

# loop through every file in the dir
root_path = '../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/'
root_dest_folder = 'source/College_Physics_Urone/'

# variable declaration
counter = 0
source_files = []
src_dirs = []
title = topic = author = editor = date = source = template_version = problem_type = attribution = outcomes = difficulty = randomization = taxonomy = ""
tags = assets = altText = image_line = []
total_start_time = time.process_time()


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
context_src = "Context"
partial_answer_src = "showPartialCorrectAnswers"

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
    question_solution = [file_content[file_content.find(marcos_end_src):file_content.find(problem_body_start_src)]]
    return {'metadata': metadata_content,
            'macros': macros,
            'question_variables': question_variables,
            'question_body': question_body,
            'question_ans': question_ans,
            'question_solution': question_solution,
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
            tags_ = item[12:-1].replace("'", "").replace('"', '').strip().split(',')
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
            question_type.append("number-input")
        elif functional_type in answer_type:
            question_type.append("functional")
        elif checkbox_type in answer_type:
            question_type.append("checkbox")
        elif text_type in answer_type:
            question_type.append("text")
        else:
            question_type.append("unknown")

    if not question_type:
        question_type.append("unknown")

    return {
        'answer_variable': answer_variable,
        'answer_type_raw': answer_type_raw,
        'question_type': question_type,
        'filename': filename}


def server(question_solution):
    # server variables
    server_imports = """
import random
import problem_bank_helpers as pbh
""".strip('\n')
    server_generate_names = "# TBD"
    server_generate_phrases = "# TBD"
    server_generate_random_var = "# N/A"
    if len(question_solution) > 0:
        server_generate_random_var = ''.join(f'# {solution.replace("$","").replace("**", "E").strip()}\n' for solution in question_solution)
    server_generate_dic = "# TBD"
    server_generate_answers = "# TBD"
    server_generate = f"""data2 = pbh.create_data2()\n# define or load names/items/objects from server files\n{server_generate_names}\n# store phrases etc\n{server_generate_phrases}\n# Randomize Variables\n{server_generate_random_var}\n# store the variables in the dictionary params\n{server_generate_dic}\n# define possible answers\n{server_generate_answers}\n# Update the data object with a new dict\ndata.update(data2)"""
    server_prepare = """pass
"""
    server_parse = """pass
"""
    server_grade = """pass
"""
    return {'imports': server_imports,
            'generate': server_generate,
            'prepare': server_prepare,
            'parse': server_parse,
            'grade': server_grade}

def yaml_dump(directory_info, metadata, question_format, image_dic, question_text, question_units, question_parts, question_solution, destination_file_path):
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
    #yaml_dict['date'] = metadata['date']
    yaml_dict['source'] = source
    yaml_dict['template_version'] = 1.3
    yaml_dict['attribution'] = 'standard'
    yaml_dict['partialCredit'] = 'true'
    yaml_dict['singleVariant'] = 'false'
    #yaml_dict['editor'] = metadata['editor']
    # yaml_dict['type'] = question_type['question_type']
    yaml_dict['outcomes'] = ['TBD']
    yaml_dict['difficulty'] = ['TBD']
    yaml_dict['randomization'] = ['TBD']
    yaml_dict['taxonomy'] = ['TBD']
    yaml_dict['span'] = ['TBD']
    yaml_dict['length'] = ['TBD']
    yaml_dict['tags'] = metadata['tags']
    yaml_dict['assets'] = image_dic['image_name'] if image_dic['image_name'] else ''
    for image in image_dic['image_name']:
        image_dir = directory_info['folder_dir'] + "/" + image
        image_path = Path(directory_info['folder_dir'] + "/" + image)
        if image_path.is_file():
            copy2(image_dir, destination_file_path)
    yaml_dict['server'] = server(question_solution)
    for part_number, part_type in zip(question_parts, question_format):
        if part_number + 1 == 0:
            part_number = str(part_number+2)
        else:
            part_number = str(part_number+1)
        yaml_dict['part' + part_number] = get_part_type(part_type)
    question_images = image_dic['image_line_md']
    Path(destination_file_path + directory_info['filename'] + ".md").write_text('---\n'
                                                                                + yaml.safe_dump(yaml_dict, sort_keys=False)
                                                                                + '---\n\n'
                                                                                + '# {{ params.vars.title }} \n\n'
                                                                                + ''.join(f'{image}\n' for image in question_images)
                                                                                + ''.join(f'\n{question}\n' for part, question in zip(question_parts, question_text) if (part == 0))
                                                                                + ''.join(f'\n## Part {part} \n{question} \n\n\n ### Answer Section\n' for part, question in zip(question_parts, question_text) if (part > 0))
                                                                                + str(question_units) + '\n\n'
                                                                                + '## pl-submission-panel \n\n\n'
                                                                                + '## pl-answer-panel \n\n\n'
                                                                                + '## Rubric \n\n\n'
                                                                                + '## Solution \n\n\n'
                                                                                + '## Comments \n\n\n')
                                                                                # + ''.join(f'{value}' for key, value in section.items())


def get_part_type(part_type):
    return {"type": part_type,
            "pl-customizations":
            {"weight": "1",
            "hide-answer-panel": "true"}
            }


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
            'image_alt_text': image_alt_text,
            'image_line_md': image_line}


def problem_extract(question_body, image_alt_text):
    hint = ''
    question_units = ''
    question_raw = []
    question_split = ''
    part_headers = []
    question_part = []

    # split question into sections based on "$PAR"
    for question in question_body:
        question_split = question.split('$PAR\n')

    # for each section of the question
    for question_section in question_split:
        # if the section is not empty
        if len(question_section) > 0:
            # remote all the \n in the section
            section_clean = question_section.replace('\n', '')
            # find and assign hint (if it exits)
            if section_clean.endswith('</strong>') or section_clean.endswith('</b>'):
                hint = section_clean
            # if hint has not been assigned (no hint exists) OR section does NOT include hint
            if not hint or hint not in section_clean:
                subsection = help_problem_extract_ans_units(section_clean)
                subsection_text = subsection['section']
                question_units = subsection['final_ans_units']
                subsection_multi_part = help_problem_extract_ans_type(subsection_text)
                subsection_multi_part_ans_type = subsection_multi_part['ans_type']
                subsection_clean = subsection_multi_part['problem_clean']
                question_raw = help_problem_extract_append(subsection_clean, question_raw)
                # remove image_alt_text from question_raw and ensure there are no empty questions
                question_raw = [question for question in question_raw if question not in image_alt_text and question]
                question_part = append_part_counter(len(question_raw)-1, part_headers)

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


def extract_problem_solution(problem_solution):
    question_solution = []

    for solution in problem_solution:
        split_solution = solution.split('\n')

        for solution_part in split_solution:
            if len(solution_part) > 0:
                # removes lines with showPartialCorrectAnswers and showHint
                if partial_answer_src not in solution_part and variables_start_src not in solution_part:
                    # removes lines with Context and TEXT(beginproblem());
                    if context_src not in solution_part and marcos_end_src not in solution_part:
                        question_solution.append(solution_part)

    return question_solution

# for loop runs based # of folders in src
for root, dirs, files in os.walk(root_path):
    # create dest file structure based on source directory
    for dir_path in src_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    # iterate through each file
    for file in files:
        if file.endswith('.pg'):
            source_files.append(os.path.join(root, file))


for source_filepath in source_files:
    try:
        dest_file_path = source_filepath[78:source_filepath.rfind('/')]
        filename = source_filepath[source_filepath.rfind('/')+1:-3]
        folder_dir = source_filepath[:source_filepath.rfind('/')]
        file_start_time = time.process_time()
        file_dir = source_filepath[source_filepath.find("Contrib"):]
        question_file = open(source_filepath, 'r')
        file_contents = question_file.read()

        file_contents_dic = split_file(file_contents)
        metadata_dic = metadata_extract(file_contents_dic['metadata'])
        dir_info = {
            'filename': filename,
            'file_dir': file_dir,
            'folder_dir': folder_dir,
            'root_dest_folder': root_dest_folder,
            'dest_file_path': dest_file_path
        }
        destination_file_path = root_dest_folder + dest_file_path + "/" + filename + "/"
        question_body = file_contents_dic['question_body']
        image_dic = image_extract(question_body)
        question_extract = problem_extract(question_body, image_dic['image_alt_text'])
        question_text = question_extract['question_text']
        question_parts = question_extract['question_parts']
        question_units = question_extract['question_units']
        question_formats = extract_problem_type(file_contents, dir_info['filename'])['question_type']
        question_solution = extract_problem_solution(file_contents_dic['question_solution'])
        Path(destination_file_path).mkdir(parents=True, exist_ok=True)
        yaml_dump(dir_info, metadata_dic, question_formats, image_dic, question_text,
                  question_units, question_parts, question_solution, destination_file_path)
        end_file_time = time.process_time()
        file_process_time = end_file_time - file_start_time
        counterString = '#' + str(counter + 1) + ' - [' + str(round(file_process_time, 5)) + '] '
        currentFile = root_dest_folder + dest_file_path + "/" + filename
        counter += 1
        print(counterString + currentFile)

    except Exception as e:
        print(e)
        pass

# ------------------------ STATS ------------------------ #
total_end_time = time.process_time()
process_time_seconds = total_end_time - total_start_time
print('total time:', round(process_time_seconds / 60, 2), 'minutes,', round(process_time_seconds, 2), 'seconds')
print('avg time per each file:', round(process_time_seconds / counter, 2), 'seconds [', counter, '] files')
