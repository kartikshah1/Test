'''
This is the file containing functions related to archiving of files.
'''

import tarfile, zipfile
import os, shutil

# Function to find the XOR of 2 objects (true if exactly one of them is not null).
def xor(a, b):
    return bool(a) != bool(b)

# Class that acts as an API for archived files. Uses the built-in tarfile and zipfile libraries to build a layer that acts as a common interface for 
# both the file types. Functions of the class are self explanatory.
class Archive(object):
    def __init__(self, name=None, fileobj=None):
        if not xor(name, fileobj):
            raise ValueError("Provide exactly one argument 'name' or 'fileobj' not both.")
        self.name = name
        self.fileobj = fileobj

        try: # check for tarfile.
            self.archive = tarfile.open(name=self.name, fileobj=self.fileobj)
            self.filetype = "tar"
            # following line is a workaround to for CRC check failed ERROR
            [a.name for a in self.archive.getmembers()]
            if fileobj:
                fileobj.seek(0)
        except tarfile.ReadError:
            pass

        try: # zipfile.
            self.archive = zipfile.ZipFile(self.name or self.fileobj)
            self.filetype = "zip"
        except zipfile.BadZipfile:
            pass
        self.is_valid = hasattr(self, 'filetype')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if hasattr(self, 'archive'):
            self.archive.close() # method implemented by both zip and tar.

    def is_archive(self):
        return self.is_valid

    def _get_tarmembers(self):
        return [a.name for a in self.archive.getmembers()]

    def _get_tarfiles(self):
        return [a.name for a in self.archive.getmembers() if a.isfile()]

    def _get_zipmembers(self):
        return self.archive.namelist()

    def _get_zipfiles(self):
        return [a for a in self.archive.namelist() if not a[-1]=="/"]

    def getfile_members(self):
        return getattr(self, "_get_{0}files".format(self.filetype))()

    def getall_members(self):
        return getattr(self, "_get_{0}members".format(self.filetype))()

    def open_file(self, name):
        ''' '''
        if self.filetype == "tar":
            return self.archive.extractfile(name)
        if self.filetype == "zip":
            return self.archive.open(name)

    def extract(self, dest):
        if self.filetype == "tar":
            self.archive.extractall(path=dest)
        if self.filetype == "zip":
            self.archive.extractall(path=dest)

# Function to return the list of files present in the input arguments. An Archive object is created with the given arguments and then the functions of
# the Archive class are used to list the files present in the Archive object (individual file or an archived file).
def get_file_name_list(name=None, fileobj=None):
    # returns name of file members of archive or file name only if not archive.
    if not xor(name, fileobj):
        raise ValueError("Provide exactly one argument 'name' or 'fileobj' not both.")

    with Archive(name=name, fileobj=fileobj) as archive:
        if archive.is_archive():
            file_list = [a.split("/")[-1] for a in archive.getfile_members()]
        else:
            file_name = (fileobj.name if fileobj else name).split("/")[-1]
            file_list = [file_name]
    if fileobj:
        fileobj.seek(0)
    return file_list

# Function to copy/extract as is the case from the source directory to the destination directory. 
# Takes as input the source and the destination paths. If the source is a single file then it is copied to the destination, else if the source path is
# an archive then it is extracted to the destination path.
def extract_or_copy(src, dest):
    # Checking if src is valid path.
    if not os.path.isfile(src):
        raise ValueError("{0} is not a valid file.")

    with Archive(name=src) as archive:
        if archive.is_archive():
            archive.extract(dest=dest)
        else:
            shutil.copy(src, dst=dest)

# Function to read a file from an archive/file.
# Takes as input the filename to be read, name of the file to be read from, and the file object of the file to be read from (either the name or the file
# object should be provided not both). If the file to be read from is a single file then the whole file is read. If it is an archive the file (given
# as readthis) is read from the archive file.
def read_file(readthis, name=None, fileobj=None):
    if not xor(name, fileobj):
        raise ValueError("Provide exactly one argument 'name' or 'fileobj' not both.")

    lines = ""
    with Archive(name=name, fileobj=fileobj) as archive:
        if archive.is_archive():
            lines = archive.open_file(readthis).readlines()
        else:
            if fileobj:
                lines = fileobj.readlines()
            else:
                fobj = open(name)
                lines = fobj.readlines()
                fobj.close()
    if fileobj:
        fileobj.seek(0)
    return lines

# Function to retrieve the files present in the filename/path given. If the input file is an archive then the files in the archive are returned.
# If the input file is a stand-alone file then it is returned.
# Takes as input the file name for which the file members are needed.
def archive_filepaths(name):
    file_names = []
    with Archive(name=name) as archive:
        if archive.is_archive():
            if archive.filetype == "tar":
                file_names = archive._get_tarfiles()
            if archive.filetype == "zip":
                file_names = archive._get_zipfiles()
        else:
            file_names.append(name.split("/")[-1])
    return file_names

# Function to copy/extract (as is the case) the file given in file_path from the source directory to the destination directory. 
# Takes as input the source and the destination paths. If the source is a single file then it is copied to the destination, else if the source path is
# an archive then the file_path file is extracted to the destination path.
def extract_or_copy_singlefile(src, dest, file_path):
    if not os.path.isfile(src):
        raise ValueError("{0} is not a valid file.")

    with Archive(name=src) as archive:
        if archive.is_archive():
            if archive.filetype == "tar":
                member = archive.archive.getmember(file_path)
                archive.archive.extract(member=member, path=dest)
            if archive.filetype == "zip":
                member = archive.archive.getinfo(file_path)
                archive.archive.extract(member=member, path=dest)
        else:
            shutil.copy(src, dst=dest)


# Function to retrieve the ith element in the array a_list.
def get_element(a_list, i):
    try:
        return a_list[i]
    except IndexError:
        return ''

# Function to retrieve the missing files in an archive file given the list of required files.
# Takes as input the list of required files, and the file object in which the missing files in an archive file.
def get_missing_files(required_files, fileobj):
    # Check if all required files are at level 1 in archive
    file_list = []
    with Archive(fileobj=fileobj) as archive:
        if archive.is_archive():
            print archive.getfile_members()
            file_list = [a.split("/")[0] for a in archive.getfile_members()]
        else:
            file_name = (fileobj.name).split("/")[-1]
            file_list = [file_name]
    if fileobj:
        fileobj.seek(0)
    missing_files = set(required_files) - set(file_list)

    # Return all files are found at level 1
    if not missing_files: 
        return

    # Check if all required files are at level 2 in archive
    with Archive(fileobj=fileobj) as archive:
        if archive.is_archive():
            file_list = [get_element(a.split("/"), 1) for a in archive.getfile_members()]
        else:
            file_name = (fileobj.name).split("/")[-1]
            file_list = [file_name]
    if fileobj:
        fileobj.seek(0)

    # Return the missing files at the level 2.
    return set(required_files) - set(file_list)