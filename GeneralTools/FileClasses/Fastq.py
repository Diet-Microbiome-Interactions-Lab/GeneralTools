import pathlib


class Fastq:
    '''
    Class for Fastq Files!
    '''
    known_extensions = ['.fastq', '.fq']
    known_compressions = ['.gz', '.gzip']
    preferred_extension = '.fastq.gz'

    available_rules = ['rule_a', 'rule_b', 'rule_d']
    outputs = ['-SIMPLIFIED.fastq', '-PASS.fastq']

    def __init__(self, file, detect_mode="medium") -> None:
        self.file_path = pathlib.Path(file)