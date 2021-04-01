### metadata
  title: example_tf
  topic: examples
  q_type: true_false
  tags: [example_q, testing]
  image: sample_question_image.png
  
### question
  Consider two numbers [a] and [b]. Is the sum of [a] + [b] less than [c]?

### solution
  import random
  
  a = random.randint(1,10)
  b = random.randint(1,10)
  c = random.randint(1,10)
  vars = [a,b,c]

  absum = a + b
  if absum<c:
    sol = True
  else:
    sol = False

  ans = [sol]
  
### notes
  This section is ignored by the file conversion system. It can be used to place any info a question creator might want to place here, such as future updates or notes for future question editors. 
  
