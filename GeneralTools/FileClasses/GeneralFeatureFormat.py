import gzip
import mimetypes
import pathlib
import pandas as pd

from BaseClasses import BioBase

def requires_validation(func):
    def wrapper(self, *args, **kwargs):
        if not self.valid:
            print("This operation cannot be performed because the object is not validated.")
            # You can also raise an exception instead of returning None
            # raise Exception("Object is not validated.")
            return None
        return func(self, *args, **kwargs)
    return wrapper

class GeneralFeatureFormat(BioBase):
    '''
    Class definition of General Feature Format version 3
    (GFF3) files.
    '''

    available_rules = ['rule_a', 'rule_b', 'rule_d']
    outputs = ['-SIMPLIFIED.fasta', ]
    ruleToOutput = {
        'rule_a': ('-SIMPLIFIED.fasta'),
        'rule_b': ('-UNSIMPLIFIED.fasta')
    }

    def __init__(self, file, detect_mode="medium") -> None:
        super().__init__(file, detect_mode)
        # Default values
        self.known_extensions.extend(['.gff', '.gff3', '.g3'])
        self.preferred_extension = '.gff3.gz'
        self.preferred_file_path = self.clean_file_name()

        # Custom stuff
        self.gffKey = {}
        self.written_output = []

        # Validation -> detect_mode=None skips this
        if detect_mode:
            self.valid_extension = self.is_known_extension()
            self.valid = self.is_valid()

    def validate(self, open_file, mode="medium"):
        if self.detect_mode == 'soft':
            print(f'DEBUG: Detecting in soft mode, only checking extension')
            return self.valid_extension
        print(f'DEBUG: Detecting comprehensively')

        line_count = 0
        valid = True
        line = next(open_file)
        while valid:
            line = line.strip()
            if line.startswith('#'):
                line = next(open_file)
                continue
            line_count += 1
            print(f'Parsing line {line_count}')
            columns = line.split('\t')
            if not len(columns) == 9:
                valid = False
                break
            seqid, source, type_, start, end, score, strand, phase, attributes = columns
            seqid = seqid.strip()
            source = source.strip()
            type_ = type_.strip()
            try:
                start = int(start)
                end = int(end)                
            except ValueError:
                print(f'DEBUG: Error in line {line_count}: Start or End invalid integer')
                valid = False
                break

            if not phase == '.':
                try:
                    phase = int(phase)
                except ValueError:
                    print(f'DEBUG: Error in line {line_count}: Phase invalid integer')
                    valid = False
                    break
            if not score == '.':                
                try:
                    score = float(score)
                except ValueError:
                    print(f'DEBUG: Error in line {line_count}: Score invalid float')
                    valid = False
                    break

            if phase not in [0, 1, 2, '.']:
                print(f'DEBUG: Error in line {line_count}: Phase must be 0, 1, 2, or "."')
                valid = False
                break

            if strand not in ['+', '-', '.']:
                print(f'DEBUG: Error in line {line_count}: Strand must be +, -, or "."')
                valid = False
                break
            self.gffKey[line_count] = (seqid, source, type_, start, end, score, strand, phase, attributes)

            try:
                line = next(open_file)
            except StopIteration:
                break
        return valid

    # ~~~ Rewriting ~~~ #
    def write_confident_gff(self, output=None):
        '''
        Here, we always want the same extension and compression: .gff3.gz
        '''
        pass
    
    def write_to_table(self, output=None):
        pass

    def do_get_longest_gene(self):
        '''
        Get the longest gene in the GFF3 file.
        '''
        return None
    # ~~~ Common Properties ~~~ #
    # @staticmethod
    # def clean_header(header: str) -> str:
    #     if header.startswith('>'):
    #         clean_header = header[1:]
    #     clean_header = clean_header.replace(' ', '_')
    #     return clean_header

    # # PROPERTIES
    # @property
    # def all_headers(self):
    #     return [v[0] for k, v in self.fastaKey.items()]


mydata = GeneralFeatureFormat('GeneralTools/FileClasses/test-files/example.gff3')
print(mydata.preferred_file_path)
print(mydata.gffKey[1])