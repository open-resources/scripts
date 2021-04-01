### metadata
  title: example_matching
  topic: examples  
  q_type: matching  
  tags: example_q, testing  
  sig_figs: N/A
  units: N/A  
  image: sample_question_image.png
  
### question
  Match the units with the correct physical quantity:
  
### solution
  import random
  
  L1 = 'Velocity'
  L2 = 'Displacement'
  L3 = 'Speed'
  L4 = 'Distance'
  L5 = 'Time'

  LHS = [ L1, L2, L3, L4, L5 ]

  R1 = 'Meters Per Second, North'
  R2 = 'Meters, North'
  R3 = 'Meters Per Second'
  R4 = 'Meters'
  R5 = 'Seconds'

  RHS = [ R1, R2, R3, R4, R5 ]

### notes
   This section is ignored by the file conversion system. It can be used to place any info a question creator might want to place here, such as future updates or notes for future question editors. For matching questions, the LHS and RHS lists should be numbers or strings. 

