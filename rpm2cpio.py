import sys

from pyrpm.rpm import RPM
from pyrpm import rpmdefs


def main(file_name):
    rpm = RPM(open(file_name, 'rb'))
    #print('is binary:', rpm.binary)
    #print('is source:', rpm.source)
    for tag, value in rpm.items().items():
        print(f'{tag} -> {value}', file=sys.stderr)
    sys.stdout.buffer.write(rpm.get_payload())
    #print(rpm.payload)


if __name__ == '__main__':
    main(sys.argv[1])
