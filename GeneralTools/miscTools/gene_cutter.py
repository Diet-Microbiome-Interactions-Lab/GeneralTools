from Bio.SeqIO.FastaIO import SimpleFastaParser

d_file = "cazy/B_celldiamond.out"
g_file = "cazy/B_cellcgc.gff"
f_file = "cazy/B_cell.fasta"


def map_diamond(d_file):
    d_mapper = {}
    with open(d_file) as file:
        line = file.readline()
        line = file.readline()
        while line:
            values = line.split('\t')
            gene_id = values[0]
            gene_start = values[8]
            gene_end = values[9]
            cazy_ids = values[1].split('|')
            for cid in cazy_ids:
                d_mapper.setdefault(cid, [])
                d_mapper[cid].append((gene_id, gene_start, gene_end))
            line = file.readline()
    return d_mapper


def map_gff(g_file):
    g_mapper = {}
    with open(g_file) as file:
        line = file.readline()
        while line:
            if line.startswith("#"):
                line = file.readline()
                continue

            values = line.strip().split('\t')
            if not values[2] == 'CAZyme':
                line = file.readline()
                continue
            gene_id = values[8].split(';')[1].split('=')[1]
            contig = values[0]
            start = values[3]
            stop = values[4]
            g_mapper[gene_id] = (contig, start, stop)
            line = file.readline()
    return g_mapper


def map_cz_to_loc(d_file, g_file, cazy):
    d_mapper = map_diamond(d_file)

    g_mapper = map_gff(g_file)
    cut_mapper = {}
    for cazyme in d_mapper.keys():
        if cazy in cazyme:

            for entry in d_mapper[cazyme]:
                locus, c_start, c_stop = entry
                if g_mapper.get(locus):
                    contig, start, stop = g_mapper[locus]
                    # cut_mapper[locus] = [(contig, start, stop)]
                    # cut_mapper[locus].append((c_start, c_stop))
                    cut_mapper.setdefault(contig, [])
                    cut_mapper[contig].append(
                        (locus, start, stop, c_start, c_stop))
        else:
            pass
    return cut_mapper


def cut_fasta(d_file, g_file, cazy, fasta, o_file, upstream, dnstream):
    cut_mapper = map_cz_to_loc(d_file, g_file, 'GH2')

    with open(o_file, 'w') as out:
        with open(fasta) as fasta_file:
            for entry in SimpleFastaParser(fasta_file):
                defline, seq = entry[0], entry[1]
                match = defline.split(' ')[0]
                if match in cut_mapper:
                    print(f'Found a match!')
                    print(cut_mapper[match])
                    start = cut_mapper[match][1]
                    end = cut_mapper[match][2]
                    seq = seq[start - upstream:end + dnstream + 1]
                    out.write(f'>{defline}\n{seq}\n')


# print(d_mapper)
# print(len(d_mapper))
# for cnt, (key, value) in enumerate(d_mapper.items()):
#     print(f'{cnt}\t{key}:\n{value}\n')
# print(d_mapper['GT2'])


cut_fasta(d_file, g_file, "GH43", f_file, 'GH43-250.fasta', 250, 250)
