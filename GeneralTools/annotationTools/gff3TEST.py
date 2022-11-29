from BCBio import GFF


gff = 'NonIsolate-Bacteroidetes_bacterium_HLUCCA01.gff3'

with open(gff) as file:
    current_genome = os.path.splitext(os.path.basename(file)[0])  # Genome var
    # Parsing each line/record of the GFF file
    for rec in GFF.parse(file):
        # Parsing the features contained within the record
        for feature in rec.features[0:3]:
            # feature.qualifiers are the values in the final column
            value = feature.qualifiers['TIGRFAM-access']
            # All fields found in each entry, but ones that are ['true']
            # actually do not have an entry; blank converts to true
            if value != ['true']:  # Print valid accessions
                print(value)
            ftype = feature.type  # Print type of feature (all CDS)
            print(rec.id)  # Print the contig it's on
        print('Next...\n\n')
