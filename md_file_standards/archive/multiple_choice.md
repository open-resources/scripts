### metadata
  title: example_mc  
  topic: examples   
  q_type: mc  
  tags: example_q, testing
  image: sample_question_image.png

### question
  A cyclist travels at [v] m/s for [t] seconds.
  How far does the cyclist travel?
  
### solution
  import random
  
  v = random.randint(2, 7)  
  t = 7
  vars = [v,t]
  

  add = v+t  
  div = v/t  
  multiply = v * t
  sub = v-t
  
  options = [add,div,multiply,sub]
  options_units = [m,m,m,m]
  
  ans = [multiply]
  ans_units = [m]
  
### notes
  This section is ignored by the file conversion system. It can be used to place any info a question creator might want to place here, such as future updates or notes for future question editors. 
