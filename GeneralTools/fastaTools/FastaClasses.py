#!/usr/bin/env python3
class BinID:

    def __init__(self, file, header=False):
        self.file = file
        self.header = header
        self.check_fields()
        self.bin_dic = self.bin_dic()

    def check_fields(self):
        line_num = 0
        with open(self.file) as _file:
            line = _file.readline()
            while line:
                line_num += 1
                length = len(line.split('\t'))
                assert length == 2, f'Invalid # of entries at line {line_num}'
                line = _file.readline()

    def bin_dic(self):
        with open(self.file) as _file:
            if self.header:
                next(_file)
            lines = _file.readlines()
            return {
                v.split('\t')[0]: v.split('\t')[1].strip() for v in lines
            }

    def contig_list(self):
        return list(self.bin_dic.keys())

    def contig_number(self):
        contigs = self.contig_list()
        return [int(contig.split('_')[1]) for contig in contigs]
