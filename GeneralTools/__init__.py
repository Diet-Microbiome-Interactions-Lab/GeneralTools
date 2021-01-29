import sys
# Below, should not need but perhaps? Mess with this later.
_bin = os.path.join(os.path.split(__file__)[0], '../GT_Bin')
sys.path.extend([_bin])


mypackage_version = '0.1-setup'

# Ensure the user is using python version >= 3
try:
    if sys.version_info.major != 3:
        sys.stderr.write(
            f"Your python version is not >= 3. You version is {sys.version_info.major}.")
        sys.exit(-1)
except Exception:
    sys.stderr.write("Failed to determine what python version is being used.")
