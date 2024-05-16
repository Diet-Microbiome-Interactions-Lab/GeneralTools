import gzip
import pathlib
import re


from GeneralTools.caragols.clix import LOGGER
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
        self.samKey = {}
        self.written_output = []
        self.preferred_file_path = self.clean_file_name()

        self.valid_extension = self.is_known_extension()
        self.valid = self.is_valid()

    def validate(self, open_file, mode="medium"):
        '''
        Takes in an open file (iterator) as validates it
        TODO: qname, rname, rnext, seq, and qual validation,
        '''
        LOGGER.debug('Detecting comprehensively')

        cigar_regex = r'^(\d+[MIDNSHP=XB])+$'
        cnt = 0

        line = next(open_file)
        while line:
            line = line.strip()
            if line.startswith('@'):
                header_line = line.split('\t')
                header_start = header_line[0]
                if header_start not in ('@HD', '@SQ', '@RG', '@PG', '@CO'):
                    LOGGER.error(f'Invalid header in line {cnt}...{line}')
                    return False
                self.samKey[cnt] = line
                cnt += 1
                line = next(open_file)
                continue
            alignment_line = line.split('\t')
            qname, flag, rname, pos = alignment_line[:4]
            mapq, cigar, rnext, pnext = alignment_line[4:8]
            tlen, seq, qual = alignment_line[8:11]
            other_fields = alignment_line[11:]
            try:
                flag = int(flag)
                pos = int(pos)
                mapq = int(mapq)
                pnext = int(pnext)
                tlen = int(tlen)
            except ValueError:
                LOGGER.error(f'Invalid int coercion in line {cnt}...{line}')
                return False
            if not re.match(cigar_regex, cigar):
                LOGGER.error(f'Invalid CIGAR score in line {cnt}...{line}')
                return False
            self.samKey[cnt] = line
            cnt += 1
            try:
                line = next(open_file).strip()
            except StopIteration:
                line = None

        return True

    # ~~~ Rewriting ~~~ #
    def do_write_confident(self, barewords, **kwargs):
        '''Write the confident SAM file to disk using default extension'''
        output = self.conf.get('output', None)
        if not output:
            output = self.preferred_file_path
        output = pathlib.Path(output)
        if output.suffix in ['.gz', '.gzip']:
            with gzip.open(str(self.preferred_file_path), 'wt') as open_file:
                for _, value in self.samKey.items():
                    output_string = value + '\n'
                    open_file.write(output_string)
        else:
            with open(str(output), 'w') as open_file:
                for _, value in self.samKey.items():
                    output_string = value + '\n'
                    open_file.write(output_string)
        data = None
        self.succeeded(msg=f"Wrote confident output to {output}", dex=data)
    

