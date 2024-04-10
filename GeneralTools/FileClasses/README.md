# Given a file, determine which rules it can enter

# Class Rules Representing a File
- Each has a 'preferred' extension and encoding
- Each has 'is_known_extension' and 'is_valid' methods
  - is_valid will call 'validate', which validates the file based on 'soft' or 'medium' modes
- Each has a method that will write a validated, preferred form as -VALIDATED{self.preferred_extension}
- Each has self.available_rules
  - ADD MORE INFO HERE
- Whenever I write a new file, I write it from the fastaKey values, not the initial file
  - This requires the file to be validated, since that's where we grabbed that internal data

### What I want to be able to do
1. $ dane myfile.fasta
   1. By default will output a verification such as: > Encoding: None, Compression: None, Valid: True, CheckSum 5AFKFKCA441, etc.
2. $ dane myfile.fasta --list-programs
   1. \> (i) make_validated; (ii) filter; (iii) trim; etc.
3. $ dane myfile.fasta filter
   1. \> Params == default
   2. How are we fully able to configure the params? At that point we may as well run the program...
   3. What about a config in the home directory specifying the the default value and params, but the user could change those as necessary
      1. This is configurability through a config file versus via a command line
4. $ dane myfile.fasta filter --cluster
5. $ dane myfile.fasta --verify --mode soft

### Notes
- Do I want some stuff to work with validation and some without? Need to think more on the validation wrapper/decorator
- Will need a class for each file type
- Will need a mapper for each rule
- To determine file types, will most likely need a hierarchical approach to guess
- When I want to extend the capabilities of the class, what's the best approach?
  - I think preference, validation, and internal permutations MUST be within the class
  - Another bucket: called an external program to do work on the file
    - For this, always write the -VALIDATED{preferred_extension}, that way we control the output's complete form --> {wildcard}-VALIDATED{preferred_extension}
      - Should I have -VALIDATED{preferred_extension} or -VALIDATED.{preferred_extension}? IDK

### TODO
1. Fasta
   1. Support for multiple files added to the class
2. Command line invocation method (probably CLIX)
3. When I add functionality, what's the easiest thing?
4. 