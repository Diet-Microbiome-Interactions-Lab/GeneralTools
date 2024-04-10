'''
This is an exploratory script that takes in an input file and determines
which snakemake rules can be ran on it. Ideally it'd be able to parse a
library of snakemake files and provide some natural-language descriptions
of what the process looks like.

The natural language description of the pipeline would be hard-coded
since we know what input and output to expect.
'''
from Fasta import Fasta
import sys

# data = Fasta('smartparser/test-files/example.fasta', detect_mode='medium')
# print(data.valid_fasta)
# data.write_to_table()
# data.write_confident_fasta()
# print(data.written_output)

if __name__ == "__main__":
    file = sys.argv[1]
    data = Fasta(file)
    print(f'Output -> Original: {data.file_name}')
    print(f'Output -> Preferred Name: {data.preferred_file_path}')
    print(f'Output -> Total seqs: {data.total_seqs}')
    print(f'Output -> Total seqlen: {data.total_seq_length}')
    print(f'Output -> Headers: {data.all_headers}')
    print(f'Output -> Sorted headers: {data.sort_fastaKey()}')
    # print(f'Output -> Rules: {data.available_rules}')
    print(f'Output -> GC Content: {data.gc_content_total}')
    print(f'Output -> GC Content: {data.filter_seqlength()}')
    print(f'Output -> GC Content: {data.n_largest_seqs(n=10)}')



# print(Workflow.__file__)
# Initialize a new workflow
# workflow = Workflow()

# Load the Snakefile
# workflow.include("smartparser/master.smk")

# Access rules (indirect and limited)
# rules = workflow.get_rules()
# for rule in rules:
#     print(rule)