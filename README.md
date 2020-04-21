# fastaprocessing
General Properties of FASTAs
Two separate lines:
1. Starts with '>' and includes identification
2. The nucleotide sequence

fasta_dict takes a single file with multiple .fasta entries and parses them into a dictionary.


# grab_removed_contigs:
Arguments required:
$ python grab_removed_contigs.py <original_bins_dir> <filtered_bins_dir> <output_filename>