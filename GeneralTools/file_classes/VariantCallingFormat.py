import gzip
import mimetypes
import pathlib
import pandas as pd

from GeneralTools.file_classes.BaseClasses import BioBase


class VariantCallingFormat(BioBase):
    '''
    Class definition of Variant Calling Format Files
    '''

    def __init__(self, file=None, detect_mode="medium") -> None:
        super().__init__(file, detect_mode, filetype='variantcallingformat')
        # Default values
        self.known_extensions.extend(['.vcf'])
        self.preferred_extension = '.vcf.gz'

        # Custom stuff
        self.vcfKey = {}
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
        '''Write the confident VCF file to disk using default extension'''
        response = 'Passing: TODO'
        self.succeeded(msg=f"{response}", dex=response)
    
    def do_write_table(self, barewords, **kwargs):
        '''Tabular VCF output'''
        response = 'Passing: TODO'
        self.succeeded(msg=f"{response}", dex=response)

    def do_get_longest_gene(self, barewords, **kwargs):
        '''Test function'''
        response = 'Test function'
        self.succeeded(msg=f"{response}", dex=response)

