from fnmatch import fnmatch
import os
import shutil
from tarfile import TarFile
from zipfile import ZipFile

from .base import BasePackager
from .downloader import Downloader


# Standard Library is not very standard.
class ArchiveFileWrapper(object):
    blacklist = ('.DS_Store', "*.pyc", "__MACOSX/*")

    def __init__(self, template_name):
        self.template_name = template_name

    def is_blacklisted(self, member_name):
        for blacklisted in self.blacklist:
            if fnmatch(member_name, blacklisted):
                return True
        return False

    def extract_members(self, download_dir):
        pardir = os.path.pardir + os.path.sep
        curdir = os.path.curdir + os.path.sep

        members = self.names()
        for member in members:
            if self.is_blacklisted(member):
                continue

            if member.startswith(curdir) or member.startswith(pardir) or member.startswith(os.path.sep):
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
                    fh.write(self.extract_file(member).read())


class ZipFileWrapper(ArchiveFileWrapper):
    def __init__(self, fh, *args, **kwargs):
        self.archive = ZipFile(fh)
        super(ZipFileWrapper, self).__init__(*args, **kwargs)

    def extract_file(self, *args, **kwargs):
        return self.archive.open(*args, **kwargs)

    def names(self):
        return self.archive.namelist()


class TarFileWrapper(ArchiveFileWrapper):
    def __init__(self, fh, *args, **kwargs):
        self.archive = TarFile(fileobj=fh)
        super(TarFileWrapper, self).__init__(*args, **kwargs)

    def extract_file(self, *args, **kwarg):
        return self.archive.extractfile(*args, **kwarg)

    def names(self):
        return self.archive.getnames()


class PackageExtractor(BasePackager):
    extract_dir = None

    def __init__(self, settings, url, template_name):
        self.template_name = template_name
        self.url = url
        super(PackageExtractor, self).__init__(settings)

    def download(self):
        response = Downloader.download(self.url)

        if self.url.endswith('.zip'):
            self.archive = ZipFileWrapper(response, self.template_name)
        elif self.url.endswith('.tgz'):
            self.archive = TarFileWrapper(response, self.template_name)
        elif self.url.endswith('.tar.gz'):
            self.archive = TarFileWrapper(response, self.template_name)

    def get_extract_dir(self):
        return os.path.join(self.settings['support_dir'], 'CACHE', self.template_name)

    def extract(self, destination=None, archive=None):
        if destination is None:
            self.extract_dir = destination = self.get_extract_dir()

        if not os.path.exists(destination):
            self.download()

            os.makedirs(destination)
            if archive is None:
                archive = self.archive
            archive.extract_members(destination)

    def cleanup(self):
        if self.extract_dir is not None:
            shutil.rmtree(self.extract_dir)
