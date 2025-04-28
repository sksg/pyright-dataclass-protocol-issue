from namespace import package1
from namespace.package2 import member

# This script imports members from two namespace packages and calls them.
# It also prints a success message to indicate that the imports were successful.
# The script is designed to be run as a standalone program.

if __name__ == "__main__":
    package1.member()
    member()
    print("Namespace packages imported successfully.")
