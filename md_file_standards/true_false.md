+++ {"ftype": "question"}
+++ {"qtype": "truefalse"}

+++ {"section": "metadata"}
"title": "Example Title"
"topic": "Example Topic"
"tag1": "Example Tag 1"
"tag2": "Example Tag 2"
"tag3": "Example Tag 3"

+++ {"section": "question_vars"}
a = numpy.random.randint(1,10)
b = numpy.random.randint(1,10)
c = numpy.random.randint(1,10)

+++ {"section": "question_text"}
Consider two numbers $a$ and $b$.
Is the sum of $a + b$ less than $c$?

+++ {"section": "question_files"}
sample_question_image.png

+++ {"section": "question_logic"}
ctest = a + b
if c<ctest:
  ans = True
else:
  ans = False
  

+++ { "section" : "answer"}
"answer": "ans"

+++ {"section" : "end"}
