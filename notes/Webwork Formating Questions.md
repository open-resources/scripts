Example .pg File:
https://github.com/open-resources/webwork-open-problem-library/blob/master/Contrib/BrockPhysics/College_Physics_Urone/2.Kinematics/NU_U17-2-08-007.pg

1. Is there any way we can figure out the problem type from the webwork syntax? i.e through the loaded Macros?

2. At what point should we send the code through the PERL processor?

3. Are the macros useful / do we need them? 

   >  Line 20:

   ```perl
   loadMacros( "PGbasicmacros.pl",
                   "MathObjects.pl",
   	        "PGauxiliaryFunctions.pl",
   	        "PGchoicemacros.pl",
   	        "PGanswermacros.pl",
                   "PG_CAPAmacros.pl",
       		"BrockPhysicsMacros.pl"
   );
   ```

4. How is latex handled on line 44-45? 

   ```perl
   \{ image( "NU_U17-2-08-007.png", width=>354, height=>225,  
   tex_size=>700, extra_html_tags=>'alt="Figure 1"' ) \}
   ```

5. How is latex handled on lines 47, 59 & 72?

  > Line 47:  `\( 100 \,\textrm{m}\)`
  >
  > Line 59:  `\(t=5 \,\textrm{s}\)`
  >
  > Line 72:  `\{ans_rule(40)\} \(\textrm{m/s}^2\)`

4. On line 42, there is a `<strong>` tag, does this part appear as bold in WebWork? If so, does WebWork support HTML tags? 

   ```html
   <strong>If you don't solve this problem correctly in $showHint tries, you can get a hint.</strong>
   ```

5. How do hints appear on WebWork? (Hint is shown above on line 42)

6. Can hints include latex?

7. Is it possible to view this example question in WebWork? (ie. a screenshot would be useful)

