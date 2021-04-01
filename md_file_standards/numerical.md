### metadata
  title: example_numeric  
  topic: examples  
  q_type: numeric  
  tags: example_q, testing  
  sig_figs: 5  
  units: m  
  
### question
  A cyclist travels at [v] m/s for [t] seconds.
  How far does the cyclist travel?
  
### solution
  v = random.randint(0, 10)  
  t = 6
  vars = [v,t]
  d = v * t
  ans = [d]
  
### imports
  random
  numpy
  
### notes
  This section is ignored by the file conversion system. But can be used to place 
  any info a question creator might want to place here, such as future updates or notes for 
  future question editors. 
