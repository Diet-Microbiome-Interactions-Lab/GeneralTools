import sys


mypackage_version = '0.1-setup'

# Ensure the user is using python version >= 3
try:
    if sys.version_info.major != 3:
        sys.stderr.write(
            f"Your python version is not >= 3. You version is {sys.version_info.major}.")
        sys.exit(-1)
except Exception:
    sys.stderr.write("Failed to determine what python version is being used.")


main_help = "This is the documentation for the main help."

programs = {
    'fastaStats': (
        ['value1', 'value2'],
        {'help': 'This is the help for fastaStats'}
    ),
    'tetranucleotideFreq': (
        ['v1', 'v2'],
        {'help': 'Help for tetranucleotideFreq'}
    ),
}
