+++ {"ftype": "question"}
+++ {"qtype": "numerical"}

+++ {"section": "metadata"}
"title": "Example Title"
"topic": "Example Topic"
"tag1": "Example Tag 1"
"tag2": "Example Tag 2"
"tag3": "Example Tag 3"

+++ {"section": "question_vars"}
# Here we are using numpy as np:
a = np.random.randint(1,10)
b = np.random.randint(1,10)


+++ {"section": "question_text"}
Consider two numbers $a and $b.
What is the sum $c = a + b$?

+++ {"section": "question_files"}
sample_question_image.png

+++ {"section": "question_logic"}
c = a + b
c_high = c
c_low = c

+++ { "section" : "answer"}
"answer": "c"
"answer_range_high": "c"
"answer_range_low": "c"

+++ {"section" : "end"}
