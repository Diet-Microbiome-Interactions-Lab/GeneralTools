import gzip
import mimetypes
import pathlib
import pandas as pd


class GFF:
    '''
    Class for Fastq Files!
    '''
    known_extensions = ['.gff', '.gff3']
    known_compressions = ['.gz', '.gzip']
    preferred_extension = '.gff3.gz'

    available_rules = ['rule_a', 'rule_b', 'rule_d']
    outputs = ['-SIMPLIFIED.gff3', '-PASS.gff3']
    ruleToOutput = {
        'rule_a': ('-SIMPLIFIED.gff3'),
        'rule_b': ('-UNSIMPLIFIED.gff3')
    }

    def __init__(self, file, detect_mode="medium") -> None:
        # Default values
        self.file_path = pathlib.Path(file)
        self.file_name = self.file_path.name
        self.detect_mode = detect_mode
        self.gffKey = {}
        self.written_output = []

        # Preferences
        self.preferred_file_path = self.clean_file_name()
        
        # Validation -> detect_mode=None skips this
        if detect_mode:
            self.valid_extension = self.is_known_extension()
            self.valid = self.is_valid()
        
        # ~~~ Preferences ~~~ #
    def clean_file_name(self) -> str:
        '''
        Always want our fasta file to end in .fastq.gz.
        For example, if a file comes in as myfile.fg, it'll be renamed to myfile.fastq.gz
        Or, if a file is fastq.txt, it'll be renamed to myfile.fastq.gz
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
        _, encoding = mimetypes.guess_type(self.file_path)

        if not encoding:  # This means no compression
            print(f'DEBUG: File is not compressed')
            # with open(str(self.file_path), 'rt') as open_file:
            #     return self.validate(iter(open_file))
        elif encoding == 'gzip':
            print(f'DEBUG: File is gzip compressed')
            # with gzip.open(str(self.file_path), 'rt') as open_file:
            #     return self.validate(iter(open_file))
        else:
            print(f'DEBUG: File is compressed but in an unknown format')
            return False
    