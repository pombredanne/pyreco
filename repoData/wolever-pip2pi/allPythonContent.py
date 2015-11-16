__FILENAME__ = commands
import os
import sys
import cgi
import shutil
import atexit
import tempfile
import textwrap
import functools
from subprocess import check_call
import pkg_resources
import glob

try:
    import wheel as _; _
    has_wheel = True
except ImportError:
    has_wheel = False

try:
    import pip
except ImportError:
    pip = None

class PipError(Exception):
    pass

def warn_wheel():
    print(
        "ERROR: .whl packages were downloaded but the wheel package "
        "is not installed, so they cannot be correctly processed.\n"
        "Install it with:\n"
        "    pip install wheel"
    )
    try:
        import setuptools
        setuptools_version = setuptools.__version__
    except ImportError:
        setuptools_version = ''
    if setuptools_version < '1.0.0':
        print(
            "WARNING: your setuptools package is out of date. This "
            "could lead to bad things.\n"
            "You should likely update it:\n"
            "    pip install -U setuptools"
        )

def dedent(text):
    return textwrap.dedent(text.lstrip("\n")).rstrip()

def maintain_cwd(f):
    @functools.wraps(f)
    def maintain_cwd_helper(*args, **kwargs):
        orig_dir = os.getcwd()
        try:
            return f(*args, **kwargs)
        finally:
            os.chdir(orig_dir)
    return maintain_cwd_helper

def egg_to_package(file):
    """ Extracts the package name from an egg::

        >>> egg_to_package("PyYAML-3.10-py2.7-macosx-10.7-x86_64.egg")
        ('PyYAML', '3.10-py2.7-macosx-10.7-x86_64.egg')
        >>> egg_to_package("python_ldap-2.3.9-py2.7-macosx-10.3-fat.egg")
        ('python-ldap', '2.3.9-py2.7-macosx-10.3-fat.egg')
    """
    dist = pkg_resources.Distribution.from_location(None, file)
    name = dist.project_name
    return (name, file[len(name)+1:])

def file_to_package(file, basedir=None):
    """ Returns the package name for a given file::

        >>> file_to_package("foo-1.2.3_rc1.tar.gz")
        ('foo', '1.2.3-rc1.tar.gz')
        >>> file_to_package("foo-bar-1.2.tgz")
        ('foo-bar', '1.2.tgz')
        >>> file_to_package("foo-bar-1.2-py27-none-any.whl")
        ('foo-bar', '1.2-py27-none-any.whl')
        >>> file_to_package("Cython-0.17.2-cp26-none-linux_x86_64.whl")
        ('Cython', '0.17.2-cp26-none-linux_x86_64.whl')
        """
    file = os.path.basename(file)
    file_ext = os.path.splitext(file)[1].lower()
    if file_ext == ".egg":
        return egg_to_package(file)

    if file_ext == ".whl":
        bits = file.rsplit("-", 4)
        split = [bits[0], "-".join(bits[1:])]
        to_safe_name = lambda x: x
    else:
        split = file.rsplit("-", 1)
        to_safe_name = pkg_resources.safe_name

    if len(split) != 2 or not split[1]:
        msg = "unexpected file name: %r " %(file, )
        msg += "(not in 'pkg-name-version.xxx' format"
        if basedir:
            msg += "; found in directory: %r" %(basedir)
        msg += ")"
        raise ValueError(msg)

    return (split[0], to_safe_name(split[1]))

def try_int(x):
    try:
        return int(x)
    except ValueError:
        return x

def pip_get_version():
    pip_dist = pkg_resources.get_distribution("pip")
    return tuple(try_int(x) for x in pip_dist.version.split("."))

def pip_run_command(pip_args):
    if pip is None:
        print("===== WARNING =====")
        print("Cannot `import pip` - falling back to the pip executable.")
        print("This will be deprecated in a future release.")
        print("Please open an issue if this will be a problem: "
              "https://github.com/wolever/pip2pi/issues")
        print("===================")
        check_call(["pip"] + pip_args)
        return

    version = pip_get_version()
    if version < (1, 1):
        raise RuntimeError("pip >= 1.1 required, but %s is installed"
                           %(version, ))
    res = pip.main(pip_args)
    if res != 0:
        raise PipError("pip failed with status %s while running: %s"
                       %(res, pip_args))


def dir2pi(argv=sys.argv):
    if len(argv) != 2:
        print(dedent("""
            usage: dir2pi PACKAGE_DIR

            Creates the directory PACKAGE_DIR/simple/ and populates it with the
            directory structure required to use with pip's --index-url.

            Assumes that PACKAGE_DIR contains a bunch of archives named
            'package-name-version.ext' (ex 'foo-2.1.tar.gz' or
            'foo-bar-1.3rc1.bz2').

            This makes the most sense if PACKAGE_DIR is somewhere inside a
            webserver's inside htdocs directory.

            For example:

                $ ls packages/
                foo-1.2.tar.gz
                $ dir2pi packages/
                $ find packages/
                packages/
                packages/foo-1.2.tar.gz
                packages/simple/
                packages/simple/foo/
                packages/simple/foo/index.html
                packages/simple/foo/foo-1.2.tar.gz
        """))
        return 1
    pkgdir = argv[1]
    if not os.path.isdir(pkgdir):
        raise ValueError("no such directory: %r" %(pkgdir, ))
    pkgdirpath = lambda *x: os.path.join(pkgdir, *x)

    shutil.rmtree(pkgdirpath("simple"), ignore_errors=True)
    os.mkdir(pkgdirpath("simple"))
    pkg_index = ("<html><head><title>Simple Index</title>"
                 "<meta name='api-version' value='2' /></head><body>\n")

    for file in os.listdir(pkgdir):
        pkg_filepath = os.path.join(pkgdir, file)
        if not os.path.isfile(pkg_filepath):
            continue
        pkg_basename = os.path.basename(file)
        if pkg_basename.startswith("."):
            continue
        pkg_name, pkg_rest = file_to_package(pkg_basename, pkgdir)
        pkg_dir = pkgdirpath("simple", pkg_name)
        if not os.path.exists(pkg_dir):
            os.mkdir(pkg_dir)
        pkg_new_basename = "-".join([pkg_name, pkg_rest])
        symlink_target = os.path.join(pkg_dir, pkg_new_basename)
        symlink_source = os.path.join("../../", pkg_basename)
        if hasattr(os, "symlink"):
            os.symlink(symlink_source, symlink_target)
        else:
            shutil.copy2(pkg_filepath, symlink_target)
        pkg_name_html = cgi.escape(pkg_name)
        pkg_index += "<a href='{0}/'>{0}</a><br />\n".format(pkg_name_html)
        with open(os.path.join(pkg_dir, "index.html"), "a") as fp:
            pkg_new_basename_html = cgi.escape(pkg_new_basename)
            fp.write("<a href='%s'>%s</a><br />\n"
                     %(pkg_new_basename_html, pkg_new_basename_html))
    pkg_index += "</body></html>\n"
    with open(pkgdirpath("simple/index.html"), "w") as fp:
        fp.write(pkg_index)
    return 0

def globall(globs):
    result = []
    for g in globs:
        result.extend(glob.glob(g))
    return result

@maintain_cwd
def pip2tgz(argv=sys.argv):
    glob_exts = ['*.whl', '*.tgz', '*.gz']

    if len(argv) < 3:
        print(dedent("""
            usage: pip2tgz OUTPUT_DIRECTORY PACKAGE_NAME ...

            Where PACKAGE_NAMES are any names accepted by pip (ex, `foo`,
            `foo==1.2`, `-r requirements.txt`).

            pip2tgz will download all packages required to install PACKAGE_NAMES and
            save them to sanely-named tarballs or wheel files in OUTPUT_DIRECTORY.

            For example:

                $ pip2tgz /var/www/packages/ -r requirements.txt foo==1.2 baz/
        """))
        return 1

    outdir = os.path.abspath(argv[1])
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    full_glob_paths = [
        os.path.join(outdir, g) for g in glob_exts
    ]
    pkg_file_set = lambda: set(globall(full_glob_paths))
    old_pkgs = pkg_file_set()

    pip_run_command(['install', '-d', outdir] + argv[2:])

    os.chdir(outdir)
    new_pkgs = pkg_file_set() - old_pkgs
    new_wheels = [ f for f in new_pkgs if f.endswith(".whl") ]
    res = handle_new_wheels(outdir, new_wheels)
    if res:
        return res

    num_pkgs = len(pkg_file_set() - old_pkgs)
    print("\nDone. %s new archives currently saved in %r." %(num_pkgs, argv[1]))
    return 0


def handle_new_wheels(outdir, new_wheels):
    """ Makes sure that, if wheel files are downloaded, their dependencies are
        correctly handled.

        This is necessary because ``pip install -d ...`` was broken
        pre-1.5.3[0].

        [0]: https://github.com/pypa/pip/issues/1617
        """
    if not new_wheels:
        return 0

    pip_version = pip_get_version()
    if pip_version >= (1, 5, 3):
        return 0

    print("")
    print("!" * 80)

    if not has_wheel:
        warn_wheel()
        # Remove the wheel files so that they will be re-downloaded and
        # their dependencies installed next time around
        for f in new_wheels:
            os.unlink(f)
        return 1

    print(dedent("""
        WARNING: Your version of pip (%s) doesn't correctly support wheel
        files. I'll do my best to work around that for now, but if possible
        you should upgrade to at least 1.5.3.
    """)) %(pip_version, )

    print("!" * 80)
    print

    for new_pkg in new_wheels:
        pkg_file_basedir = os.path.abspath(os.path.dirname(new_pkg))
        pkg_name, _ = file_to_package(new_pkg)
        pip_run_command([
            '-q', 'wheel', '-w', outdir,
            '--find-links', pkg_file_basedir,
            pkg_name,
        ])

def pip2pi(argv=sys.argv):
    if len(argv) < 3:
        print(dedent("""
            usage: pip2pi TARGET PACKAGE_NAME ...

            Combines pip2tgz and dir2pi, adding PACKAGE_NAME to package index
            TARGET.

            If TARGET contains ':' it will be treated as a remote path. The
            package index will be built locally then rsync will be used to copy
            it to the remote host.

            For example, to create a remote index:

                $ pip2pi example.com:/var/www/packages/ -r requirements.txt

            Or to create a local index:

                $ pip2pi ~/Sites/packages/ foo==1.2
        """))
        return 1

    target = argv[1]
    pip_packages = argv[2:]
    if ":" in target:
        is_remote = True
        working_dir = tempfile.mkdtemp(prefix="pip2pi-working-dir")
        atexit.register(lambda: shutil.rmtree(working_dir))
    else:
        is_remote = False
        working_dir = os.path.abspath(target)

    res = pip2tgz([argv[0], working_dir] + pip_packages)
    if res:
        print("pip2tgz returned an error; aborting.")
        return res

    res = dir2pi([argv[0], working_dir])
    if res:
        print("dir2pi returned an error; aborting.")
        return res

    if is_remote:
        print("copying temporary index at %r to %r..." %(working_dir, target))
        check_call([
            "rsync",
            "--recursive", "--progress", "--links",
            working_dir + "/", target + "/",
        ])
    return 0

########NEW FILE########
__FILENAME__ = test
#!/usr/bin/env python
import os
import sys
try:
    from urllib import unquote
except ImportError: # python3
    from urllib.parse import unquote

import random
import shutil
import doctest
import tempfile
import unittest
import threading
import posixpath
import subprocess

try:
    from SocketServer import ThreadingMixIn
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError: # python 3
    from socketserver import ThreadingMixIn
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PKG_BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")
sys.path.append(PKG_BASE_PATH)

from libpip2pi import commands as pip2pi_commands

class chdir(object):
    """ A drop-in replacement for ``os.chdir`` which also acts as a context
        manager.

        >>> old_cwd = os.getcwd()
        >>> with chdir("/usr/"):
        ...     print("current dir:", os.getcwd())
        ...
        current dir: /usr
        >>> os.getcwd() == old_cwd
        True
        >>> x = chdir("/usr/")
        >>> os.getcwd()
        '/usr'
        >>> x
        chdir('/usr/', old_path='...')
        >>> x.unchdir()
        >>> os.getcwd() == old_cwd
        True
        """

    def __init__(self, new_path, old_path=None):
        self.old_path = old_path or os.getcwd()
        self.new_path = new_path
        self.chdir()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.unchdir()

    def chdir(self):
        os.chdir(self.new_path)

    def unchdir(self):
        os.chdir(self.old_path)

    def __repr__(self):
        return "%s(%r, old_path=%r)" %(
            type(self).__name__, self.new_path, self.old_path,
        )


class Pip2PiRequestHandler(SimpleHTTPRequestHandler):
    base_path = os.path.join(BASE_PATH, "assets/")

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path


class Pip2PiHeavyTests(unittest.TestCase):
    SERVER_PORT = random.randint(10000, 40000)

    class BackgroundIt(threading.Thread):
        server = None
        def run(self):
            self.server.serve_forever()

    class ThreadingServer(ThreadingMixIn, HTTPServer):
        pass

    @classmethod
    def setUpClass(cls):
        cls._server_thread = cls.BackgroundIt()
        cls.server = cls.ThreadingServer(("127.0.0.1", cls.SERVER_PORT),
                                         Pip2PiRequestHandler)
        cls._server_thread.server = cls.server
        cls._server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def setUp(self):
        os.chdir(BASE_PATH)
        self._temp_dir = None
        print("\n" + "-" * 70)

    def tearDown(self):
        if self._temp_dir is not None:
            shutil.rmtree(self._temp_dir)

    def assertDirsEqual(self, a, b):
        res = subprocess.call(["diff", "-x", "*", "-r", a, b])
        if res:
            with chdir(a):
                print("1st directory:", a)
                subprocess.call(["find", "."])
            with chdir(b):
                print("2nd directory:", b)
                subprocess.call(["find", "."])
            raise AssertionError("Directories %r and %r differ! (see errors "
                                 "printed to stdout)" %(a, b))

    @property
    def temp_dir(self):
        if self._temp_dir is None:
            self._temp_dir = tempfile.mkdtemp(prefix="pip2pi-tests")
        return self._temp_dir

    @property
    def index_url(self):
        return "--index-url=http://127.0.0.1:%s/simple/" %(self.SERVER_PORT, )

    def exc(self, cmd, args):
        print("Running %s with: %s" %(cmd, args))
        return getattr(pip2pi_commands, cmd)([cmd] + args)

    def test_requirements_txt(self):
        res = self.exc("pip2pi", [
            self.temp_dir,
            self.index_url,
            "-r", "test_requirements_txt/requirements.txt",
        ])
        self.assertEqual(res, 0)
        self.assertDirsEqual("test_requirements_txt/expected/", self.temp_dir)

    def test_eggs_in_packages(self):
        shutil.copy("test_eggs_in_packages/fish-1.1-py2.7.egg", self.temp_dir)
        self.exc("dir2pi", [self.temp_dir])
        self.assertDirsEqual("test_eggs_in_packages/", self.temp_dir)

    def test_wheels(self):
        res = self.exc("pip2tgz", [
            self.temp_dir,
            self.index_url,
            "-r", "test_wheels/requirements.txt",
        ])
        self.assertEqual(res, 0)
        self.assertDirsEqual('test_wheels/expected/', self.temp_dir)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(pip2pi_commands))
    return tests


if __name__ == "__main__":
    unittest.main()

########NEW FILE########