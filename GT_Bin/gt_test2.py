#!/Users/ddeemer/.pyenv/versions/3.9.0/bin/python
from GeneralTools.Utilities.command_line import find_executable
import json
import os
import sys


def main(executable):
    return find_executable(executable)


print(os.listdir())
with open('pipeline-config.json') as f:
    data = json.load(f)

execs = data['executables']
cpus = data['cpus']
print(cpus)
slurm = data['run']
print(slurm)

# for val in execs:
#     a = main(val)
#     print(a)

# if __name__ == '__main__':
#     print(main(sys.argv[1]))
