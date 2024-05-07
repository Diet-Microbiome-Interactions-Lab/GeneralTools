import gzip
import pathlib

import pandas as pd

from GeneralTools.FileClasses.BaseClasses import BioBase


def requires_validation(func):
    def wrapper(self, *args, **kwargs):
        if not self.valid:
            print("This operation cannot be performed because the object is not validated.")
            # You can also raise an exception instead of returning None
            # raise Exception("Object is not validated.")
            return None
        return func(self, *args, **kwargs)
    return wrapper

class Fasta(BioBase):
    '''
    Class for Fasta Files
    Want it to determine if it's gzip or not
    '''
    # known_extensions = ['.fna', '.fasta', '.fa']
    # known_compressions = ['.gz', '.gzip']
    # preferred_extension = '.fasta.gz'

    available_rules = ['rule_a', 'rule_b', 'rule_d']
    outputs = ['-SIMPLIFIED.fasta', ]
    ruleToOutput = {
        'rule_a': ('-SIMPLIFIED.fasta'),
        'rule_b': ('-UNSIMPLIFIED.fasta')
    }

    def __init__(self, file=None, detect_mode="medium") -> None:
        super().__init__(file=file, detect_mode=detect_mode, filetype='fasta')
        # Default values
        self.known_extensions.extend(['.fna', '.fasta', '.fa'])
        self.preferred_extension = '.fasta.gz'

        # Custom stuff
        self.fastaKey = {}
        self.written_output = []
        self.preferred_file_path = self.clean_file_name()

        self.valid_extension = self.is_known_extension()
        self.valid = self.is_valid()

    def validate(self, open_file, mode="medium"):
        '''
        Validate the Fasta file and hydrate self.fastaKey, a dictionary of the fasta file
        in the form:
        {entry_index: (header, sequence)}
        '''
        if self.detect_mode == 'soft':
            print(f'DEBUG: Detecting in soft mode, only checking extension')
            return self.valid_extension
        print(f'DEBUG: Detecting comprehensively')

        valid_chars = set('ATGCNatgcn')
        prev_header = False
        current_header = ''
        current_seq = ''
        cnt = 0

        line = next(open_file)
        while line:
            line = line.strip()
            if not line:
                line = next(open_file)
                continue
            if line.startswith('>'):
                cnt += 1
                current_header = line.strip()
                current_seq = ''
                if prev_header:
                    print('Error: 2 headers in a row')
                    self.fastaKey = {}
                    return False
                prev_header = True
                line = next(open_file)
            else:
                while line and not line.startswith('>'):
                    if not set(line).issubset(valid_chars):
                        print(f'Error: Line has invalid character...{line}')
                        return False
                    else:
                        current_seq += line.strip()
                        try:
                            line = next(open_file).strip()
                        except StopIteration:
                            line = None
                self.fastaKey[cnt] = (self.clean_header(current_header), current_seq.upper())

                prev_header = False

        return True

    # ~~~ Rewriting ~~~ #
    def do_write_confident(self, barewords, **kwargs):
        '''
        Here, we always want the same extension and compression: .fasta.gz
        We also want to ensure only ATGCN and each sequence is on 1 line
        '''
        if not self.valid:
            response = 'File is not valid'
            self.failed(msg=f"{response}")
        

        output = self.conf.get('output', None)
        if not output:
            output = self.preferred_file_path
        output = pathlib.Path(output)
        if output.suffix in ['.gz', '.gzip']:
            with gzip.open(str(self.preferred_file_path), 'wt') as open_file:
                for key, value in self.fastaKey.items():
                    open_file.write(f'>{value[0]}\n{value[1]}\n')
            # self.written_output.append(('write_confident_fasta', self.preferred_file_path))  # Provenance
        else:
            with open(str(output), 'w') as open_file:
                for _, value in self.fastaKey.items():
                    open_file.write(f'>{value[0]}\n{value[1]}\n')
            # self.written_output.append(('write_confident_fasta', self.preferred_file_path))  # Provenance
        response = 'Wrote the output file'
        self.succeeded(msg=f"{response}", dex=response)
    
    def do_write_table(self, barewords, **kwargs):
        '''Tabular output'''
        if not self.valid:
            response = 'File is not valid'
            self.failed(msg=f"{response}")

        print(self.conf.show())
        output = self.conf.get('output', None)
        if not output:
            print(f'Self.file_path: {self.file_path}')
            output = self.file_path.stem + '-VALIDATED.txt.gz'
        output = pathlib.Path(output)

        print(f'Writing to output...{output}')
        if output.suffix in ['.gz', '.gzip']:
            with gzip.open(str(output), 'wt') as open_file:
                for _, value in self.fastaKey.items():
                    open_file.write(f'{value[0]},{value[1]}\n')
        else:
            with open(str(output), 'w') as open_file:
                for key, value in self.fastaKey.items():
                    open_file.write(f'{value[0]},{value[1]}\n')
        response = 'Wrote the output file'
        self.succeeded(msg=f"{response}", dex=response)
        

    # ~~~ Common Properties ~~~ #
    @staticmethod
    def clean_header(header: str) -> str:
        if header.startswith('>'):
            clean_header = header[1:]
        clean_header = clean_header.replace(' ', '_')
        return clean_header

    # PROPERTIES
    def do_all_headers(self, barewords, **kwargs):
        '''Return all headers to standard out'''
        response = [v[0] for k, v in self.fastaKey.items()]
        self.succeeded(msg=f"{response}", dex=response)

    def do_all_seqs(self, barewords, **kwargs):
        '''Return all sequences to standard out'''
        response = [v[1] for k, v in self.fastaKey.items()]
        self.succeeded(msg=f"{response}", dex=response)
    
    def do_gc_content(self, barewords, **kwargs):
        '''Return the GC content of each sequence in the fasta file'''
        gcContent = {}
        for cnt, items in self.fastaKey.items():
            seq = items[1].upper()
            gc_count = seq.count('G') + seq.count('C')
            percent = round((gc_count) / len(seq), 3)
            gcContent[cnt] = (items[0], percent)
        response = gcContent
        self.succeeded(msg=f"{response}", dex=response)

    def do_gc_content_total(self, barewords, **kwargs):
        '''Return the total GC content of the fasta file'''
        values = []
        for cnt, items in self.fastaKey.items():
            seq = items[1].upper()
            gc_count = seq.count('G') + seq.count('C')
            gc_content = (gc_count / len(seq)) * 100 if len(seq) > 0 else 0
            values.append(round(gc_content, 3))
        response = sum(values) / len(values) if values else 0
        self.succeeded(msg=f"{response}", dex=response)

    def do_total_seq_length(self, barewords, **kwargs):
        '''Return the total length of all sequences in the fasta file'''
        response =  sum([len(v[1]) for k, v in self.fastaKey.items() ])
        self.succeeded(msg=f"{response}", dex=response)

    def do_total_seqs(self, barewords, **kwargs):
        '''Return the total number of sequences in the fasta file'''
        print(f'Running inside of total_seqs with {barewords} and {kwargs}')
        response = len(self.fastaKey.keys())
        self.succeeded(msg=f"Total sequences: {response}", dex=response)
    
    def total_seq_length(self, barewords, **kwargs):
        '''Return the total length of all sequences in the fasta file'''
        response = sum([len(v[1]) for k, v in self.fastaKey.items() ])
        self.succeeded(msg=f"{response}", dex=response)

    
    # Misc. Actions and Functionality
    def do_filter_seqlength(self, barewords, **kwargs):
        '''Filter the sequences by length, default is 2000'''

        seqlength = self.conf.get('seqlen', 2000)
        output = self.conf.get('output', None)
        if not output:
            output = self.file_path.with_name(f'{self.basename}-FILTERED-{seqlength}bp.txt')

        with open(output, 'wt') as open_file:
            for cnt, items in self.fastaKey.items():
                if len(items[1]) > seqlength:
                    writeline = f'>{items[0]}\n{items[1]}\n'
                    open_file.write(writeline)
        response = f'Processed with seqlength of {seqlength} and wrote to output: {output}'
        self.succeeded(msg=f"{response}", dex=response)
    
    def do_n_largest_seqs(self, barewords, **kwargs):
        '''Return the n largest sequences in the fasta file'''
        n = int(self.conf.get('n', 10))
        output = self.conf.get('output', None)
        if not output:
            output = self.file_path.with_name(f'{self.basename}-LARGEST-{n}.txt')

        sorted_values = self.sorted_fasta
        with open(output, 'wt') as open_file:
            for count, (index, (header, seq)) in enumerate(sorted_values.items()):
                print(f'Testing {seq} >= {n}')
                if count >= n:
                    break
                writeline = f'>{header}\n{seq}\n'
                print(f'Writeline: {writeline}')
                open_file.write(writeline)
        response = 'Success: File created'
        self.succeeded(msg=f"{response}", dex=response)

    def do_seq_length(self, barewords, **kwargs):
        '''Return the length of a specific sequence'''
        response = {(k, v[0]): len(v[1]) for k, v in self.fastaKey.items()}
        self.succeeded(msg=f"{response}", dex=response)

    @property
    def sorted_fasta(self):
        ascending = self.conf.get('ascending', False)
        if not ascending:
            return dict(sorted(self.fastaKey.items(), key=lambda item: item[1][0].lower()))
        return dict(sorted(self.fastaKey.items(), key=lambda item: item[1][0].lower()), reverse=True)
    