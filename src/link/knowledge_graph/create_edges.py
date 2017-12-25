from signal import signal, SIGPIPE, SIG_DFL
import sys

from link.utils import read_object_tuples


def main():
    print('":START_ID",":TYPE",":END_ID"')
    for object_tuple in read_object_tuples(sys.stdin):
        object_tuple = (
            object_tuple[0],
            object_tuple[1].replace('#', '_'),
            object_tuple[2]
        )
        print('"' + '","'.join(object_tuple) + '"')


if __name__ == '__main__':
    signal(SIGPIPE, SIG_DFL)
    main()
