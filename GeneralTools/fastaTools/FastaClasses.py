class BinID:

    def __init__(self, file, header=False):
        self.file = file
        self.check_fields()
        self.bin_dic = self.bin_dic()

    def check_fields(self):
        line_num = 0
        with open(self.file) as _file:
            line = _file.readline()
            while line:
                line_num += 1
                assert len(line.split('\t')) == 2,
                    f'Invalid # of entries at line {line_num}'
            line = _file.readline()

    def bin_dic(self):
        ret_dic = {}
        with open(self.file) as _file:
            if self.header:
                next(_file)
            lines = _file.readline()
            return {
                v.split('\t')[0]: v.split('\t')[1].strip() for v in lines
            }
