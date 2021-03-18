### metadata
  title: example_mc
  topic: examples
  q_type: multiple_choice
  tags: [example_q, testing]
  
### question
  A cyclist travels at (v) m/s for [t] seconds.
  How far does the cyclist travel?
  
### parameters
  v = 1,
  t = 1
  
### solution
  - 0
  - 2
  - *1*
  - 3

+++ {"ftype": "question"}
+++ {"qtype": "multiplechoice"}

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
d = numpy.random.randint(1,10)
e = numpy.random.randint(1,10)
f = numpy.random.randint(1,10)

+++ {"section": "question_text"}
Consider two numbers $a$ and $b$.
What is the sum of $a$ and $b$?

+++ {"section": "question_files"}
sample_question_image.png

+++ {"section": "question_logic"}
ans = a + b

+++ {"section": "possible_answers"}
"a1" = ans
"a2 = c
"a2 = d
"a2 = e
"a2 = f


+++ { "section" : "answer"}
"answer": "a1"

+++ {"section" : "end"}
