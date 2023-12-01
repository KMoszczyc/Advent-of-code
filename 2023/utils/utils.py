def read_file(path):
    with open(path, "r") as f:
        return f.read().split('\n')


def find_all(s, p):
    """Yields all the positions of the pattern p in the string s."""
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i + 1)
