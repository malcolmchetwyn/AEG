import re


def check_documentation(filename):
    with open(filename, 'r') as file:
        content = file.read()
        # Simple keyword check for demo purposes
        keywords = ['architecture', 'compliance', 'standards']
        for keyword in keywords:
            if re.search(rf'\b{keyword}\b', content, re.IGNORECASE):
                print(f"Found keyword '{keyword}' in {filename}")
            else:
                print(f"Keyword '{keyword}' not found in {filename}")


if __name__ == "__main__":
    check_documentation('README.md')
