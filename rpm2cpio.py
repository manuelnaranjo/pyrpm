import sys

from pyrpm.rpm import RPM


def main(file_name):
    rpm = RPM(open(file_name, 'rb'))
    for tag, value in rpm.items().items():
        print(f'{tag} -> {value}', file=sys.stderr)
    sys.stdout.buffer.write(rpm.get_payload())


if __name__ == '__main__':
    main(sys.argv[1])
