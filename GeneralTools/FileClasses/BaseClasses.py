import gzip
import mimetypes
import pathlib

from caragols.lib import clix

class BioBase(clix.App):
    '''
    Base class for biological data classes.
    '''
    known_compressions = ['.gz', '.gzip']
    known_extensions = []

    def __init__(self, file, detect_mode="medium"):
        super().__init__(run_mode="cli")
        self.file = file
        self.file_path = pathlib.Path(file)
        self.file_name = self.file_path.name
        self.detect_mode = detect_mode
    
            # ~~~ Preferences ~~~ #
    
    def clean_file_name(self) -> str:
        '''
        Always want our fastq file to end in .fastq.gz.
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
            with open(str(self.file_path), 'rt') as open_file:
                return self.validate(iter(open_file))
        #TODO Add dynamic opening from self.known_compressions
        elif encoding == 'gzip':
            print(f'DEBUG: File is gzip compressed')
            with gzip.open(str(self.file_path), 'rt') as open_file:
                return self.validate(iter(open_file))
        else:
            print(f'DEBUG: File is compressed but in an unknown format')
            return False