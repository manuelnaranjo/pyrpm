import sys
import tarfile
import os

from io import BytesIO, StringIO
from pyrpm.rpm import RPM
from pyrpm.cpio import CpioArchive, CpioEntry


class Rpm2Tar:
    def __init__(self, file_list, output=sys.stdout.buffer):
        self.file_list = file_list
        tmpfile = BytesIO()
        self.tarfile = tarfile.open(mode='x', fileobj=tmpfile)
        self.entries = set()
        self._process_rpm_files()
        tmpfile.seek(0)
        output.write(tmpfile.read())

    def _process_rpm_files(self):
        for name in self.file_list:
            self._process_rpm_file(name)

    def _process_rpm_file(self, name):
        rpm = RPM(open(name, 'rb'))
        cpio = rpm.get_payload()
        cpio = CpioArchive(fileobj=BytesIO(cpio))
        for entry in cpio:
            self._process_cpio_file(entry)
        cpio.close()

    def add_parent(self, tar_entry: tarfile.TarInfo):
        name = tar_entry.name
        if name[-1] == '/': # remove trailing to get to the root
            name = name[:-1]
        parent_name = os.path.dirname(name)
        if parent_name in self.entries or len(parent_name) < 2: # ignore . and /
            return
        parent_tar_entry = tarfile.TarInfo(parent_name + "/")
        parent_tar_entry.devmajor = tar_entry.devmajor
        parent_tar_entry.devminor = tar_entry.devminor
        parent_tar_entry.mtime = tar_entry.mtime
        mode = (tar_entry.mode | ((0o444 & tar_entry.mode) >> 2))
        parent_tar_entry.mode = mode
        parent_tar_entry.uid = tar_entry.uid
        parent_tar_entry.gid = tar_entry.gid
        parent_tar_entry.type = tarfile.DIRTYPE

        self.entries.add(parent_name)
        if len(os.path.split(parent_name)) > 1:
            self.add_parent(parent_tar_entry)
        self.tarfile.addfile(parent_tar_entry)

    def _process_cpio_file(self, inp: CpioEntry):
        if inp.name in self.entries:
            print(f'ignoring duplicate {inp.name}', file=sys.stderr)
            return

        tar_entry = tarfile.TarInfo(inp.name)
        tar_entry.devmajor = inp.devmajor
        tar_entry.devminor = inp.devminor
        tar_entry.mtime = inp.mtime
        tar_entry.mode = inp.file_mode()
        tar_entry.uid = inp.uid
        tar_entry.gid = inp.gid
        if not inp.is_symlink() and not inp.is_regular_file() and not inp.is_directory():
            print(f'ignoring {inp.name} not sure how to treat it {oct(inp.mode)}', file=sys.stderr)
            return
        self.entries.add(inp.name)
        self.add_parent(tar_entry)
        if inp.is_directory():
            tar_entry.type = tarfile.DIRTYPE
            self.tarfile.addfile(tar_entry)
            return
        if inp.is_symlink():
            tar_entry.type = tarfile.SYMTYPE
            tar_entry.linkname = inp.read().decode('utf-8')
            self.tarfile.addfile(tar_entry)
        elif inp.is_regular_file():
            tar_entry.type = tarfile.REGTYPE
            tar_entry.size = inp.size
            self.tarfile.addfile(tar_entry, BytesIO(inp.read()))


def main(files):
    tar = Rpm2Tar(file_list=files)
    print(tar)

if __name__ == '__main__':
    main(sys.argv[1:])
