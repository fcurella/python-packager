import os
from tarfile import TarFile
from zipfile import ZipFile

from .base import BasePackager


# Standard Library is not very standard.
class ZipFileWrapper(object):
    def __init__(self, fh):
        self.archive = ZipFile(fh)
        super(ZipFileWrapper, self).__init__()

    def extract_file(self, *args, **kwargs):
        return self.archive.open(*args, **kwargs)

    def names(self):
        return self.archive.namelist()


class TarFileWrapper(object):
    def __init__(self, fh):
        self.archive = TarFile(fileobj=fh)
        super(TarFileWrapper, self).__init__()

    def extract_file(self, *args, **kwarg):
        return self.archive.extractfile(*args, **kwarg)

    def names(self):
        return self.archive.getnames()


class PackageExtractor(BasePackager):
    def __init__(self, settings, url, response, template_name):
        super(PackageExtractor, self).__init__(settings)
        if url.endswith('.zip'):
            self.archive = ZipFileWrapper(response)
        elif url.endswith('.tgz'):
            self.archive = TarFileWrapper(response)
        elif url.endswith('.tar.gz'):
            self.archive = TarFileWrapper(response)

        self.template_name = template_name

    def extract_members(self, archive, download_dir):
        members = archive.names()
        for member in members:
            if member.startswith('./') or member.startswith('../') or member.startswith('/'):
                raise RuntimeError("Archive is unsafe.")

            if member.split(os.path.sep)[0].startswith(self.template_name):
                try:
                    outfile = os.path.sep.join(member.split(os.path.sep)[1:])
                except IndexError:
                    continue
            else:
                outfile = member
            outpath = os.path.join(download_dir, outfile)

            if not outpath.endswith(os.path.sep):
                parent_dir = os.path.dirname(outpath)
                if not os.path.exists(parent_dir):
                    os.makedirs(parent_dir)
                with open(outpath, 'w') as fh:
                    fh.write(archive.extract_file(member).read())

    def extract(self, download_dir, archive=None):
        if archive is None:
            archive = self.archive
        self.extract_members(archive, download_dir)
