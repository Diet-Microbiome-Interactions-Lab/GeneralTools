import json
import os
import time

file = 'UofM-Fastqs.txt'


def getLinks(file):
    links = []
    with open(file) as json_file:
        data = json.load(json_file)

    prefix = '/gridftp/ena'
    for record in data:
        try:
            reads = record['fastq_ftp'].split(';')
        except ValueError:
            reads = [record['fastq_ftp']]

        for read in reads:
            values = read.split('/')
            links.append(os.path.join(prefix, '/'.join(values[2:])))
    return links


print(len(getLinks(file)))


def makeBatchFile(file, output):
    ep1 = 'fd9c190c-b824-11e9-98d7-0a63aa6b37da'
    ep2 = '9115718a-0f57-11eb-893c-0a5521ff3f4b'
    links = getLinks(file)

    dest = '/scratch/bell/ddeemer/Rumino/fastqs/'
    with open(output, 'w') as out:
        out.write('# Header File: Downloading all Fastq Files - Dane 14Jun22\n')
        for link in links:
            filename = os.path.basename(link)
            writeline = f'{link}\t{os.path.join(dest, filename)}\n'
            out.write(writeline)


def runDownloads(file):
    ep1 = 'fd9c190c-b824-11e9-98d7-0a63aa6b37da'
    ep2 = '9115718a-0f57-11eb-893c-0a5521ff3f4b'
    dest = '/scratch/bell/ddeemer/Rumino/fastq/'
    links = getLinks(file)

    for cnt, link in enumerate(links):
        print(f'{cnt}: Submitting next link: {link}')
        filename = os.path.basename(link)
        cur_dest = os.path.join(dest, filename)
        cmd = f'globus transfer {ep1}:{link} {ep2}:{cur_dest}'
        os.system(cmd)
        time.sleep(10)
    return 0


# if __name__ == '__main__':
#     runDownloads(file)
