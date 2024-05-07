import gzip
import mimetypes
import pathlib
import sys

from GeneralTools.caragols import clix

class BioBase(clix.App):
    '''
    Base class for biological data classes.
    '''
    known_compressions = ['.gz', '.gzip']
    known_extensions = []

    def __init__(self, file=None, detect_mode="medium", filetype=None) -> None:
        self.detect_mode = detect_mode
        super().__init__(run_mode="cli", name="fileflux", filetype=filetype)
        self.form = self.conf.get('report.form', 'prose')
        # self._mode comes from clix.App
        if self._mode == 'debug':
            print(f'\n#~~~~~~~~~~ Starting BioBase Init ~~~~~~~~~~#')
            print(f'BioBase:\n{self.conf.show()}')
        self.file = self.conf.get('file', None)

        if not self.matched:
            sys.stdout.write(self.report.formatted(self.form))
            sys.stdout.write('\n')
            self.done()
            if self.report.status.indicates_failure:
                sys.exit(1)
            else:
                sys.exit(0)

        if self.file:
            self.file_path = pathlib.Path(self.file)
            self.file_name = self.file_path.name
        elif 'help' in self.matched[0]:  # Dont necessarily need a file to show help
            self.run()
        else:
            message = f'ERROR: No file provided. Please add file via: $ python3 main.py file: example.fasta'
            self.failed(
                msg=f"Total sequences: {message}", dex=message)
            sys.stdout.write(self.report.formatted(self.form))
            sys.stdout.write('\n')
            self.done()
            if self.report.status.indicates_failure:
                sys.exit(1)
            else:
                sys.exit(0)
        if self._mode == 'debug':
            print('#~~~~~~~~~~ Finished BioBase Init ~~~~~~~~~~#\n')
    
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
    
    def file_not_valid_report(self):
        print(f'File is not valid according to validation')
        message = f'File is not valid according to validation'
        self.failed(
            msg=f"{message}", dex=message)
        sys.stdout.write(self.report.formatted(self.form))
        sys.stdout.write('\n')
        self.done()
        if self.report.status.indicates_failure:
            sys.exit(1)
        else:
            sys.exit(0)
    
    def do_valid(self, barewords, **kwargs):
        '''Check to see if the file is valid, meaning it has been parsed and the contents are correct'''
        response = self.valid
        self.succeeded(
            msg=f"File was scrubbed and found to be {response}", dex=response)
        return 0