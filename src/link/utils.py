import logging
import mmap
import re


resource='<http://nl\.dbpedia\.org/resource/(.*)>'
relation='<.*/(.*)>'
literal='"(.*)"(.*)'
literal_pattern='^%s %s %s .$' % (resource, relation, literal)
literal_prog = re.compile(literal_pattern)
object_pattern='^%s %s %s .$' % (resource, relation, resource)
object_prog = re.compile(object_pattern)


def read_literal_tuples(f):
    for line in f:
        if not line.startswith('#'):
            result = literal_prog.match(line)
            yield (
                result.group(1).split('__')[0],
                result.group(2),
                result.group(3) \
                    .replace('\\\'', '\'') \
                    .replace('\\"', '"') \
                    .replace('\\\\', '\\')
            )


def read_object_tuples(f):
    for line in f:
        if not line.startswith('#'):
            result = object_prog.match(line)
            if result is not None:
                yield (
                    result.group(1).split('__')[0],
                    result.group(2),
                    result.group(3).split('__')[0] \
                        .replace('\\\'', '\'') \
                        .replace('\\"', '"') \
                        .replace('\\\\', '\\')
                )


def get_num_lines(filename):
    f = open(filename, 'rb')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    return lines


def enable_logging():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.INFO
    )
