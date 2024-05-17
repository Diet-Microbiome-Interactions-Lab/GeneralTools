import os
import sys

# direct = sys.argv[1]
# output = sys.argv[2]


# def main(direct, output):
#     '''
#     '''
#     with open(output, 'w') as out:
#         for file in os.listdir(direct):
#             if file.endswith('.HMM'):
#                 full_file = os.path.join(direct, file)
#                 with open(full_file) as file:
#                     line = file.readline()
#                     while line:
#                         if line.startswith('NAME'):
#                             name = line.split()[1]
#                         if line.startswith('DESC'):
#                             desc = ' '.join(line.split()[1:])
#                             out.write(f"{name}\t{desc}\n")
#                             break
#                         line = file.readline()


def main(results, translate, output):
    '''
    '''

    source = 'TIGRFAM'

    translater = {}
    with open(translate) as tran:
        line = tran.readline()
        while line:
            values = line.strip().split('\t')
            translater[values[0]] = values[1]
            line = tran.readline()

    with open(output, 'w') as out:
        header = f"gene_callers_id\tsource\taccession\tfunction\te_value\n"
        out.write(header)
        with open(results) as file:
            line = file.readline()
            while line:
                if line.startswith('#'):
                    pass
                else:
                    values = line.split()
                    gene_id = values[0]
                    assert int(gene_id), 'Not an integer?'
                    tigr = values[2]
                    assert tigr.startswith('TIGR'), 'Invalid Tigr name!'
                    e_val = values[4]
                    function = translater[tigr]
                    writeline = f"{gene_id}\t{source}\t{tigr}\t{function}\t{e_val}\n"
                    out.write(writeline)
                line = file.readline()


results = sys.argv[1]
translate = sys.argv[2]
output = sys.argv[3]

if __name__ == '__main__':
    main(results, translate, output)
