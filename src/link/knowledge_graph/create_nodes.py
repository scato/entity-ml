from signal import signal, SIGPIPE, SIG_DFL
import sys

from link.utils import read_literal_tuples


def main():
    print('"id:ID","label"')
    for label_tuple in read_literal_tuples(sys.stdin):
        label_tuple = (
            label_tuple[0],
            label_tuple[2] \
                .replace('"', '""') \
                .replace('\\', '\\\\')
        )
        print('"' + '","'.join(label_tuple) + '"')


if __name__ == '__main__':
    signal(SIGPIPE, SIG_DFL)
    main()
