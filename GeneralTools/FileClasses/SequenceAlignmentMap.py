import gzip
import mimetypes
import pathlib
import pandas as pd

from GeneralTools.FileClasses.BaseClasses import BioBase


class SequenceAlignmentMap(BioBase):
    '''
    Class definition of Sequence Alignment Mapper Files
    '''

    def __init__(self, file=None, detect_mode="medium") -> None:
        super().__init__(file, detect_mode, filetype='sequencealignmentformat')
        # Default values
        self.known_extensions.extend(['.sam', '.sm', '.s'])
        self.preferred_extension = '.sam.gz'

        # Custom stuff
        self.gffKey = {}
        self.written_output = []
        self.preferred_file_path = self.clean_file_name()

        self.valid_extension = self.is_known_extension()
        self.valid = self.is_valid()

    def validate(self, open_file, mode="medium"):
        '''
        Takes in an open file (iterator) as validates it
        TODO: Take in a string or something instead?
        Generator/iterator is the best way to handle large files
        '''
        return True

    # ~~~ Rewriting ~~~ #
    def do_write_confident(self, barewords, **kwargs):
        '''Write the confident SAM file to disk using default extension'''
        data = 'Passing: TODO'
        self.succeeded(msg=f"{data}", dex=data)
    
    def do_write_table(self, barewords, **kwargs):
        '''Tabular SAM output'''
        data = 'Passing: TODO'
        self.succeeded(msg=f"{data}", dex=data)

    def do_get_longest_gene(self, barewords, **kwargs):
        '''Test function'''
        data = 'Test function'
        self.succeeded(msg=f"{data}", dex=data)

