import gzip
import mimetypes
import pathlib
import pandas as pd

def requires_validation(func):
    def wrapper(self, *args, **kwargs):
        if not self.valid:
            print("This operation cannot be performed because the object is not validated.")
            # You can also raise an exception instead of returning None
            # raise Exception("Object is not validated.")
            return None
        return func(self, *args, **kwargs)
    return wrapper

class GcFile(BaseClass):
    pass

class Fasta:
    '''
    Class for Fasta Files
    Want it to determine if it's gzip or not
    '''
    known_extensions = ['.fna', '.fasta', '.fa']
    known_compressions = ['.gz', '.gzip']
    preferred_extension = '.fasta.gz'

    available_rules = ['rule_a', 'rule_b', 'rule_d']
    outputs = ['-SIMPLIFIED.fasta', ]
    ruleToOutput = {
        'rule_a': ('-SIMPLIFIED.fasta'),
        'rule_b': ('-UNSIMPLIFIED.fasta')
    }


    def __init__(self, file, detect_mode="medium") -> None:
        # Default values
        self.file_path = pathlib.Path(file)
        self.file_name = self.file_path.name
        self.detect_mode = detect_mode
        self.fastaKey = {}
        self.written_output = []

        # Preferences
        self.preferred_file_path = self.clean_file_name()
        
        # Validation -> detect_mode=None skips this
        if detect_mode:
            self.valid_extension = self.is_known_extension()
            self.valid = self.is_valid()

    # Experimental rule
    def create_output(self, rule):
        pass
    
    # ~~~ Preferences ~~~ #
    def clean_file_name(self) -> str:
        '''
        Always want our fasta file to end in .fasta.gz.
        For example, if a file comes in as myfile.fna, it'll be renamed to myfile.fasta.gz
        Or, if a file is myfile.txt, it'll be renamed to myfile.fasta.gz
        '''
        suffixes = self.file_path.suffixes
        self.basename = self.file_path.stem
        if suffixes[-1] in self.known_compressions:
            if len(suffixes) > 1 and suffixes[-2] in self.known_extensions:
                self.basename = pathlib.Path(self.basename).stem
                return self.file_path.with_name(f'{self.basename}-VALIDATED{self.preferred_extension}')
            return None
        return self.file_path.with_name(f'{self.basename}-VALIDATED{self.preferred_extension}')

    # ~~~ Validation Stuff ~~~ #
    def is_known_extension(self) -> bool:
        '''
        Is there a known extension of the file?
        '''
        suffixes = self.file_path.suffixes
        if suffixes[-1] in self.known_compressions:
            return len(suffixes) > 1 and suffixes[-2] in self.known_extensions
        else:
            return suffixes[-1] in self.known_extensions

    def is_valid(self) -> bool:
        file_type, encoding = mimetypes.guess_type(self.file_path)

        if not encoding:  # This means no compression
            print(f'DEBUG: File is not compressed')
            with open(str(self.file_path), 'rt') as open_file:
                return self.validate(iter(open_file))
        elif encoding == 'gzip':
            print(f'DEBUG: File is gzip compressed')
            with gzip.open(str(self.file_path), 'rt') as open_file:
                return self.validate(iter(open_file))
        else:
            print(f'DEBUG: File is compressed but in an unknown format')
            return False
    
    def validate(self, open_file, mode="medium"):
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
    def write_confident_fasta(self, output=None):
        '''
        Here, we always want the same extension and compression: .fasta.gz
        We also want to ensure only ATGCN and each sequence is on 1 line
        '''
        if not self.valid:
            print(f'Error: Is not a valid fasta file')
            return None
        if not self.detect_mode or self.detect_mode == 'soft':
            print(f'Error: Cannot write a new file without medium+ verification')
            return None

        if output:
            with gzip.open(str(output), 'wt') as open_file:
                for key, value in self.fastaKey.items():
                    open_file.write(f'>{value[0]}\n{value[1]}\n')
            self.written_output.append(('write_confident_fasta', self.preferred_file_path))  # Provenance
        else:
            with gzip.open(str(self.preferred_file_path), 'wt') as open_file:
                for key, value in self.fastaKey.items():
                    open_file.write(f'>{value[0]}\n{value[1]}\n')
            self.written_output.append(('write_confident_fasta', self.preferred_file_path))  # Provenance
        
        return 0
    
    def write_to_table(self, output=None):
        if not self.valid:
            print(f'Error: Is not a valid fasta file')
            return None
        if not self.detect_mode or self.detect_mode == 'soft':
            print(f'Error: Cannot write a new file without medium+ verification')
            return None
        
        table_name = self.file_path.with_name(f'{self.basename}-VALIDATED.txt')
        data = [[v[0], v[1]] for k, v in self.fastaKey.items()]
        df = pd.DataFrame(data=data, columns=['Defline', 'Sequence'])
        if output:
            df.to_csv(str(output))
            self.written_output.append(('to_table', str(output)))
        else:
            df.to_csv(table_name)
            self.written_output.append(('to_table', str(table_name)))
        return 0

    # ~~~ Common Properties ~~~ #
    @staticmethod
    def clean_header(header: str) -> str:
        if header.startswith('>'):
            clean_header = header[1:]
        clean_header = clean_header.replace(' ', '_')
        return clean_header

    # PROPERTIES
    @property
    def all_headers(self):
        return [v[0] for k, v in self.fastaKey.items()]

    @property
    def all_seqs(self):
        return [v[1] for k, v in self.fastaKey.items()]
    
    @property
    def gc_content(self):
        gcContent = {}
        for cnt, items in self.fastaKey.items():
            seq = items[1].upper()
            gc_count = seq.count('G') + seq.count('C')
            percent = round((gc_count) / len(seq), 3)
            gcContent[cnt] = (items[0], percent)
        return gcContent

    @property
    def gc_content_total(self):
        values = []
        for cnt, items in self.fastaKey.items():
            seq = items[1].upper()
            gc_count = seq.count('G') + seq.count('C')
            gc_content = (gc_count / len(seq)) * 100 if len(seq) > 0 else 0
            values.append(round(gc_content, 3))
        return sum(values) / len(values) if values else 0

    @property
    def total_seq_length(self):
        return sum([len(v[1]) for k, v in self.fastaKey.items() ])

    @property
    def total_seqs(self):
        return len(self.fastaKey.keys())
    
    @property
    def get_total_t(self):
        '''
        Grab the total ts
        '''
        return 400
    
    # Misc. Actions and Functionality
    @requires_validation
    def filter_seqlength(self, seqlen=2000, output=None):
        if not output:
            output = self.file_path.with_name(f'{self.basename}-FILTERED.txt')

        with open(output, 'wt') as open_file:
            for cnt, items in self.fastaKey.items():
                if len(items[1]) > seqlen:
                    writeline = f'>{items[0]}\n{items[1]}\n'
                    open_file.write(writeline)
        return 0
    
    @requires_validation
    def n_largest_seqs(self, n=10, output=None):
        if not output:
            output = self.file_path.with_name(f'{self.basename}-{n}LARGEST.txt')

        sorted_values = self.sort_fastaKey(ascending=False)
        print(f'Sorted values: {sorted_values}')
        with open(output, 'wt') as open_file:
            for index, (_, items) in enumerate(sorted_values.items()):
                print(f'Index: {index} --> {items}')
                print(f'Testing {index} >= {n}')
                if index >= n:
                    break
                writeline = f'>{items[0]}\n{items[1]}\n'
                print(f'Writeline: {writeline}')
                open_file.write(writeline)
        return 'Success: File created'

    def sort_fastaKey(self, ascending=True):
        if ascending:
            return dict(sorted(self.fastaKey.items(), key=lambda item: item[1][0].lower()))
        return dict(sorted(self.fastaKey.items(), key=lambda item: item[1][0].lower(), reverse=True))
        
