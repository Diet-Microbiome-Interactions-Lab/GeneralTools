import gzip
import mimetypes
import pathlib
import pandas as pd


from BaseClasses import BioBase


# class Fastq(BioBase):
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

    def __init__(self, file=None, detect_mode="medium") -> None:
        super().__init__(file=file, detect_mode=detect_mode)
        # Default value extension
        self.known_extensions.extend(['.fastq', '.fq'])
        self.preferred_extension = '.fastq.gz'
        self.preferred_file_path = self.clean_file_name()

        # Custom stuff
        self.fastqKey = {}
        self.written_output = []

        # Validation -> detect_mode=None skips this
        if detect_mode:
            self.valid_extension = self.is_known_extension()
            self.valid = self.is_valid()
        
        # if not self.valid:
        #     self.file_not_valid_report()

        # Below, self.run comes from clix.App. We need to call it first to get the configuration
        # Where do we want to run the program? Probably from the main
        # self.run()

    # ~~~ Validation Stuff ~~~ #
    def validate(self, open_file, mode="medium"):
        if self.detect_mode == 'soft':
            # print(f'DEBUG: Detecting in soft mode, only checking extension')
            return self.valid_extension
        # print(f'DEBUG: Detecting comprehensively')

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
    
    def do_test(self, barewords, **kwargs):
        '''
        Test function!!!\n
        This function is for testing purposes only.
        '''
        response = 'Test function called'
        self.succeeded(
            msg=f"Total sequences: {response}", dex=response)
        return 0
    
    def do_something_funny(self, barewords, **kwargs):
        '''
        Help for telling a joke
        '''
        response = 'Heres a joke...knock knock!'
        self.succeeded(msg=response, dex=response)
        return 0

    
    def do_grab_first_record(self, barewords, **kwargs):
        '''
        Returns the first record in the fastq file
        '''
        response = self.fastqKey[0]
        self.succeeded(
            msg=f"{response}", dex=response)
        return 0

    def do_all_headers(self, barewords, **kwargs):
        '''
        Shows all headers in the fastq file
        '''
        response = [v[0] for k, v in self.fastqKey.items()]
        self.succeeded(
            msg=f"{response}", dex=response)
        return 0
    
    def do_seqlengths(self, barewords, **kwargs):
        '''
        Return all of the seqlengths in the fastq file
        '''
        seqlens = set()
        for k, v in self.fastqKey.items():
            seqlens.add(len(v[1]))
        response = seqlens
        self.succeeded(
            msg=f"{response}", dex=response)
        return 0
    
    def do_gc_content(self, barewords, **kwargs):
        '''
        Return the GC content for each record in the fastq file
        '''
        gcContent = {}
        for cnt, items in self.fastqKey.items():
            seq = items[1].upper()
            gc_count = seq.count('G') + seq.count('C')
            percent = round((gc_count) / len(seq), 3)
            gcContent[cnt] = (items[0], percent)
        response = gcContent
        self.succeeded(
            msg=f"{response}", dex=response)
        return 0

    def do_gc_content_total(self, barewords, **kwargs):
        '''
        Get the total GC content for the fastq file
        '''
        values = []
        for cnt, items in self.fastqKey.items():
            seq = items[1].upper()
            gc_count = seq.count('G') + seq.count('C')
            gc_content = (gc_count / len(seq)) * 100 if len(seq) > 0 else 0
            values.append(round(gc_content, 3))
        value = sum(values) / len(values) if values else 0
        response = f'Returned a GC value of {value}'
        self.succeeded(
            msg=f"{response}", dex=response)
        return 0
