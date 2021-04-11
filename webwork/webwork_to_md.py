from pathlib import Path
import yaml

problem_file_name = 'NU_U17-2-03-005.pg'  # short answer
path = '../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/2.Kinematics/' + problem_file_name

file = open(path, 'r')
file_contents = file.read()
title, author, source, problem_type, tags, outcomes, assets, server = "", "", "", "", "", "", "", ""

for item in file_contents.split("\n"):
    if "## TitleText1" in item:
        title = item[item.find("(") + 1:item.find(")")].replace("'", "")
    if "## AuthorText1" in item:
        author = item[item.find("(") + 1:item.find(")")].replace("'", "")
