import gzip
import mimetypes
import pathlib
import pandas as pd


from BaseClasses import BioBase


class Fastq(BioBase):
    '''
    Class for Fastq Files!
    '''
    available_rules = ['rule_a', 'rule_b', 'rule_d']
    outputs = ['-SIMPLIFIED.fastq', '-PASS.fastq']
    ruleToOutput = {
        'rule_a': ('-SIMPLIFIED.fasta'),
        'rule_b': ('-UNSIMPLIFIED.fasta')
    }

    def __init__(self, file, detect_mode="medium") -> None:
        # Custom stuff
        self.fastqKey = {}
        self.written_output = []
        super().__init__(file, detect_mode)
        # Default value extension
        self.known_extensions.extend(['.fastq', '.fq'])
        self.preferred_extension = '.fastq.gz'
        self.preferred_file_path = self.clean_file_name()

        

        # Validation -> detect_mode=None skips this
        if detect_mode:
            self.valid_extension = self.is_known_extension()
            self.valid = self.is_valid()

        # Specific
        self.fastaKey = {}
        self.written_output = []

    # ~~~ Validation Stuff ~~~ #
    def validate(self, open_file, mode="medium"):
        if self.detect_mode == 'soft':
            print(f'DEBUG: Detecting in soft mode, only checking extension')
            return self.valid_extension
        print(f'DEBUG: Detecting comprehensively')

        # Content Stuff
        valid_chars = set('ATGCNatgcn')
        valid_qchars = '!"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        valid_qchars += "'"

        line_count = 0
        valid = True
        line = next(open_file)

        entry_count = 0
        while valid:
            line = line.strip()
            line_count += 1
            if line_count % 4 == 1:
                if not line.startswith('@'):
                    print(f"DEBUG: Error on line {line_count}: Header line must start with '@'")
                    valid = False
                    return False
                current_header_1 = line
            elif line_count % 4 == 2:
                if not set(line).issubset(valid_chars):
                    print(f"DEBUG: Error on line {line_count}: Sequence line contains invalid characters")
                    valid = False
                seqlen = len(line)
                current_seq = line
            elif line_count % 4 == 3:
                if not line.startswith('+'):
                    print(f"DEBUG: Error on line {line_count}: Separator line must start with '+'")
                    valid = False
                current_header_2 = line
            elif line_count % 4 == 0:
                if not set(line).issubset(valid_qchars):
                    print(f"DEBUG: Error on line {line_count}: Quality line contains invalid characters")
                    valid = False
                elif seqlen != len(line):
                    print(f"DEBUG: Error on line {line_count}: Quality line length does not match sequence line length")
                    valid = False
                else:
                    current_qual = line
                    seqlen = -1
                    self.fastqKey[entry_count] = (current_header_1, current_seq, current_header_2, current_qual )
                    entry_count += 1
            try:
                line = next(open_file)
            except StopIteration:
                if line_count % 4 != 0:
                    print(f"DEBUG: Error on line {line_count}: File ended in the middle of a record")
                    valid = False
                break


        return valid
    
    def do_something_funny(self):
        '''
        Help for telling a joke
        '''
        print(f'Heres a joke...knock knock!')
    
    def do_grab_first_record(self):
        '''
        Returns the first record in the fastq file
        '''
        return 'Example first key'

    def do_all_headers(self):
        '''
        Shows all headers in the fastq file
        '''
        return [v[0] for k, v in self.fastqKey.items()]
    
    def do_seqlengths(self):
        '''
        Return all of the seqlengths in the fastq file
        '''
        seqlens = set()
        for k, v in self.fastqKey.items():
            seqlens.add(len(v[1]))
        return seqlens
    
    def do_gc_content(self):
        '''
        Return the GC content for each record in the fastq file
        '''
        gcContent = {}
        for cnt, items in self.fastqKey.items():
            seq = items[1].upper()
            gc_count = seq.count('G') + seq.count('C')
            percent = round((gc_count) / len(seq), 3)
            gcContent[cnt] = (items[0], percent)
        return gcContent

    def do_gc_content_total(self):
        '''
        Get the total GC content for the fastq file
        '''
        values = []
        for cnt, items in self.fastqKey.items():
            seq = items[1].upper()
            gc_count = seq.count('G') + seq.count('C')
            gc_content = (gc_count / len(seq)) * 100 if len(seq) > 0 else 0
            values.append(round(gc_content, 3))
        return sum(values) / len(values) if values else 0


myfile = 'GeneralTools/FileClasses/test-files/example.fastq'

fastq = Fastq(myfile)
print(fastq.valid)
# print(fastq.fastqKey)
print(fastq.do_all_headers)
print(fastq.seqlengths)
print(fastq.gc_content_total)

if __name__ == "__main__":
    pass