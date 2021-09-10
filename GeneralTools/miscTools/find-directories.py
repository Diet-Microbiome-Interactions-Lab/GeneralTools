'''
'''
import glob
import os


class UserInformation:
    '''
    '''

    def __init__(self, line):
        try:
            len(line.strip().split()) == 8
            self.permissions, self.number, self.name = line.split()[0:3]
            self.size, self.month, self.day, self.time, self.username = line.split()[
                3:]
        except ValueError:
            pass


class Privileges(UserInformation):
    '''
    Capture privilege information
    '''

    def __init__(self, line):
        super().__init__(line)
        self.ownervalues = self.permissions[1:4]
        self.groupvalues = self.permissions[4:7]
        self.allvalues = self.permissions[7:10]

        # for cnt, values in enumerate(['Owner', 'Group', 'All'])
        #     self.read = values[0]
        #     self.write = values[0]
        #     self.execute = values[0]


myline = 'drwxr-xr-x   14 aabdulw    20 Jun 30 20:56 aabdulw'

myval = UserInformation(myline)
permis = Privileges(myline)
# print(permis.ownervalues)

with open('test.txt') as f:
    line = f.readline()
    while line:
        User = Privileges(line)
        if User.allvalues[0] == 'r':
            print(f"Here: {line}")
        line = f.readline()

# myval.privileges(Group='all')
# print(myval.read)
