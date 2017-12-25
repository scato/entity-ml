from signal import signal, SIGPIPE, SIG_DFL
import sys

from link.utils import read_literal_tuples


def main():
    i = 0
    for label_tuple in read_literal_tuples(sys.stdin):
        label_tuple = (
            label_tuple[0],
            label_tuple[2] \
                .replace('"', '""') \
                .replace('\\', '\\\\')
        )
        print('{"index":{"_index":"dictionary","_id":%s}}' % (i))
        print('{"id":"%s","label":"%s"}' % label_tuple)
        i += 1


if __name__ == '__main__':
    signal(SIGPIPE, SIG_DFL)
    main()
