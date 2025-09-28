import re
import sys


def check_file(filename):
    with open(filename) as f:
        content = f.read()
        if re.search(r"hashlib\.md5", content):
            print(f"Weak hash found in {filename}")
        if re.search(r"print\(.*password", content):
            print(f"Sensitive info logged in {filename}")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        check_file(arg)
