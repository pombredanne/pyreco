__FILENAME__ = log
# coding=utf-8
import glob2
import os
import logging

logger = logging.getLogger("psdash.log")

class LogError(Exception):
    pass

class LogSearcher(object):
    # Read 200 bytes extra to not miss keywords split between buffers
    EXTRA_SIZE = 200

    def __init__(self, log):
        self.log = log

    @property
    def position(self):
        return self.log.fp.tell()

    def __repr__(self):
        return "<LogSearcher filename=%s, file-pos=%d>" % (
            self.log.filename, self.position
        )

    def _read(self, length=None, offset=None):
        """
        This method reads from the log file starting at the given offset and
        reads at most the number of bytes specified by the length parameter.

        This method will make sure to not alter the file's position when returned.
        """
        if not length:
            length = self.log.buffer_size

        pos = self.position
        if offset:
            self.log.fp.seek(offset)
        buf = self.log.fp.read(length).decode('utf8')
        self.log.fp.seek(pos)
        return buf

    def _get_buffers(self):
        while self.position:
            # make sure to not read what's already been read
            # when we're at the beginning of the file.
            length = min(self.log.buffer_size, self.position)
            self.log.fp.seek(-length, os.SEEK_CUR)
            buf = self._read(length=length)

            if not buf:
                raise StopIteration

            yield buf

    def _read_result(self, position):
        # try to get the result in the middle of a buffer length of content.
        read_before = self.log.buffer_size / 2
        offset = max(position - read_before, 0)
        respos = position if offset == 0 else read_before
        return respos, self._read(offset=offset)

    def reached_end(self):
        return self.position == 0

    def reset(self):
        self.log.fp.seek(0, os.SEEK_END)

    def find_next(self, text):
        """
        Find text in log file from current position

        returns a tuple containing:
            absolute position,
            position in result buffer,
            result buffer (the actual file contents)
        """
        lastbuf = ""
        for buf in self._get_buffers():
            buf += lastbuf
            i = buf.rfind(text.decode('utf8'))
            if i >= 0:
                # get position of the found text
                pos = self.position + i
                # try to read a whole buffer length with the result in the middle
                respos, resbuf = self._read_result(pos)
                # move the file position to the result pos to make sure we start from
                # this position to not miss results in the same buffer.
                self.log.fp.seek(pos)
                return pos, respos, resbuf

            lastbuf = buf[:self.EXTRA_SIZE]
        return -1, -1, ""


class LogReader(object):
    BUFFER_SIZE = 8192

    def __init__(self, filename, buffer_size=BUFFER_SIZE):
        self.filename = filename
        self.fp = open(filename, "r")
        self.buffer_size = buffer_size
        self.searcher = LogSearcher(self)

    def __repr__(self):
        return "<LogReader filename=%s, file-pos=%d>" % (
            self.filename, self.fp.tell()
        )

    def set_tail_position(self):
        stat = os.fstat(self.fp.fileno())
        if stat.st_size >= self.buffer_size:
            self.fp.seek(-self.buffer_size, os.SEEK_END)
        else:
            self.fp.seek(0)

    def read(self):
        buf = self.fp.read(self.buffer_size)
        return buf

    def search(self, text):
        return self.searcher.find_next(text)

    def close(self):
        self.fp.close()


class Logs(object):
    def __init__(self):
        self.available = set()
        self.readers = {}

    def add_available(self, filename):
        # quick verification that it exists and can be read
        try:
            filename = filename.decode("utf-8")
            f = open(filename)
            f.close()
        except IOError as e:
            raise LogError("Could not read log file '%s' (%s)" % (filename, e))

        logger.debug("Adding log file %s", filename)

        return self.available.add(filename)

    def remove_available(self, filename):
        self.available.remove(filename)

    def get_available(self):
        return [self.get(filename) for filename in self.available]

    def clear_available(self):
        self.available = set()

    def add_patterns(self, patterns):
        for p in patterns:
            for log_file in glob2.iglob(p):
                try:
                    self.add_available(log_file)
                except LogError as e:
                    logger.warning(e)

        logger.info("Added %d log file(s)", len(self.available))

    def clear(self):
        for r in self.readers.itervalues():
            r.close()
        self.readers = {}

    def create(self, filename, key=None):
        if filename not in self.available:
            raise KeyError("No log with filename '%s' is available" % filename)

        key = (filename, key)
        r = LogReader(filename)
        self.readers[key] = r
        return r

    def get(self, filename, key=None):
        reader_key = (filename, key)
        if reader_key not in self.readers:
            return self.create(filename, key)
        else:
            return self.readers.get(reader_key)

########NEW FILE########
__FILENAME__ = net
# coding=utf-8

import socket
import struct
import array
import fcntl
import psutil
import time
import sys
 

class NetIOCounters(object):
    def __init__(self, pernic=True):
        self.last_req = None
        self.last_req_time = None
        self.pernic = pernic

    def _get_net_io_counters(self):
        """
        Fetch io counters from psutil and transform it to
        dicts with the additional attributes defaulted
        """
        counters = psutil.net_io_counters(pernic=self.pernic)

        res = {}
        for name, io in counters.iteritems():
            res[name] = io._asdict()
            res[name].update({"tx_per_sec": 0, "rx_per_sec": 0})

        return res

    def _set_last_request(self, counters):
        self.last_req = counters
        self.last_req_time = time.time()

    def get(self):
        return self.last_req

    def update(self):
        counters = self._get_net_io_counters()

        if not self.last_req:
            self._set_last_request(counters)
            return counters

        time_delta = time.time() - self.last_req_time
        if not time_delta:
            return counters

        for name, io in counters.iteritems():
            last_io = self.last_req.get(name)
            if not last_io:
                continue

            counters[name].update({
                "rx_per_sec": (io["bytes_recv"] - last_io["bytes_recv"]) / time_delta,
                "tx_per_sec": (io["bytes_sent"] - last_io["bytes_sent"]) / time_delta
            })

        self._set_last_request(counters)

        return counters


def get_interface_addresses(max_interfaces=10):
    """
    Get addresses of available network interfaces.
    See netdevice(7) and ioctl(2) for details.

    Returns a list of dicts
    """

    SIOCGIFCONF = 0x8912

    if sys.maxsize > (1 << 31):
        ifreq = struct.Struct("16sH2xI16x")
    else:
        ifreq = struct.Struct("16sHI8x")

    # create request param struct
    ifconf = struct.Struct("iL")
    bufsize = ifreq.size * max_interfaces
    buf = array.array("B", "\0" * bufsize)
    ifconf_val = ifconf.pack(bufsize, buf.buffer_info()[0])

    # make ioctl request
    sock = socket.socket()
    ifconf_res = fcntl.ioctl(sock.fileno(), SIOCGIFCONF, ifconf_val)
    sock.close()

    buflen, _ = ifconf.unpack(ifconf_res)
    resbuf = buf.tostring()

    addresses = []
    for x in xrange(buflen / ifreq.size):
        # read the size of the struct from the result buffer
        # and unpack it.
        start = x * ifreq.size
        stop = start + ifreq.size
        name, family, address = ifreq.unpack(resbuf[start:stop])

        # transform the address to it's string representation
        ip = socket.inet_ntoa(struct.pack("I", address))
        name = name.rstrip("\0")

        addr = {
            "name": name,
            "family": family,
            "ip": ip
        }

        addresses.append(addr)

    return addresses

########NEW FILE########
__FILENAME__ = web
# coding=utf-8
import argparse
from flask import Flask, render_template, request, session, jsonify, Response, Blueprint
import logging
import psutil
import platform
import socket
import os
from datetime import datetime
import time
import threading
import uuid
import locale
from log import Logs
from net import NetIOCounters, get_interface_addresses

logs = Logs()
net_io_counters = NetIOCounters()
logger = logging.getLogger("psdash.web")


def get_disks(all_partitions=False):
    disks = [
        (dp, psutil.disk_usage(dp.mountpoint))
        for dp in psutil.disk_partitions(all_partitions)
    ]
    disks.sort(key=lambda d: d[1].total, reverse=True)
    return disks


def get_users():
    users = []
    for u in psutil.get_users():
        dt = datetime.fromtimestamp(u.started)
        user = {
            "name": u.name.decode("utf-8"),
            "terminal": u.terminal,
            "started": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "host": u.host.decode("utf-8")
        }

        users.append(user)
    return users


def get_network_interfaces():
    io_counters = net_io_counters.get()
    addresses = get_interface_addresses()

    for inf in addresses:
        inf.update(io_counters.get(inf["name"], {}))

    return addresses


app = Flask(__name__)
app.config.from_envvar("PSDASH_CONFIG", silent=True)

app_url_prefix = app.config.get("PSDASH_URL_PREFIX")
if app_url_prefix:
    app_url_prefix = "/" + app_url_prefix.strip("/")

psdashapp = Blueprint(
    "psdash",
    __name__,
    url_prefix=app_url_prefix,
    static_folder="static"
)

# If the secret key is not read from the config just set it to something.
if not app.secret_key:
    app.secret_key = "whatisthissourcery"


allowed_remote_addrs = []


# Patch the built-in, but not working, filesizeformat filter for now.
# See https://github.com/mitsuhiko/jinja2/pull/59 for more info.
@app.template_filter()
def filesizeformat(value, binary=False):
    """Format the value like a 'human-readable' file size (i.e. 13 kB,
    4.1 MB, 102 Bytes, etc).  Per default decimal prefixes are used (Mega,
    Giga, etc.), if the second parameter is set to `True` the binary
    prefixes are used (Mebi, Gibi).
    """
    bytes = float(value)
    base = binary and 1024 or 1000
    prefixes = [
        (binary and 'KiB' or 'kB'),
        (binary and 'MiB' or 'MB'),
        (binary and 'GiB' or 'GB'),
        (binary and 'TiB' or 'TB'),
        (binary and 'PiB' or 'PB'),
        (binary and 'EiB' or 'EB'),
        (binary and 'ZiB' or 'ZB'),
        (binary and 'YiB' or 'YB')
    ]
    if bytes == 1:
        return '1 Byte'
    elif bytes < base:
        return '%d Bytes' % bytes
    else:
        for i, prefix in enumerate(prefixes):
            unit = base ** (i + 2)
            if bytes < unit:
                return '%.1f %s' % ((base * bytes / unit), prefix)
        return '%.1f %s' % ((base * bytes / unit), prefix)


@app.before_first_request
def load_allowed_remote_addrs():
    addrs = app.config.get("PSDASH_ALLOWED_REMOTE_ADDRESSES")
    if addrs:
        app.logger.info("Setting up allowed remote addresses list.")
        for addr in addrs.split(","):
            allowed_remote_addrs.append(addr.strip())


@app.before_request
def check_access():
    if allowed_remote_addrs:
        if request.remote_addr not in allowed_remote_addrs:
            app.logger.info(
                "Returning 401 for client %s as address is not in allowed addresses.",
                request.remote_addr
            )
            app.logger.debug("Allowed addresses: %s", allowed_remote_addrs)
            return "Access denied", 401

    username = app.config.get("PSDASH_AUTH_USERNAME")
    password = app.config.get("PSDASH_AUTH_PASSWORD")
    if username and password:
        auth = request.authorization
        if not auth or auth.username != username or auth.password != password:
            return Response(
                "Access deined",
                401,
                {'WWW-Authenticate': 'Basic realm="psDash login required"'}
            )


@app.before_request
def setup_client_id():
    if "client_id" not in session:
        client_id = uuid.uuid4()
        app.logger.debug("Creating id for client: %s", client_id)
        session["client_id"] = client_id


@psdashapp.errorhandler(404)
def page_not_found(e):
    app.logger.debug("Client tried to load an unknown route: %s", e)
    return render_template("error.html", error="Page not found."), 404


@psdashapp.errorhandler(psutil.AccessDenied)
def access_denied(e):
    errmsg = "Access denied to %s (pid %d)." % (e.name, e.pid)
    return render_template("error.html", error=errmsg), 401


@psdashapp.errorhandler(psutil.NoSuchProcess)
def access_denied(e):
    errmsg = "No process with pid %d was found." % e.pid
    return render_template("error.html", error=errmsg), 401


@psdashapp.route("/")
def index():
    load_avg = os.getloadavg()
    uptime = datetime.now() - datetime.fromtimestamp(psutil.get_boot_time())
    disks = get_disks()
    users = get_users()

    netifs = get_network_interfaces()
    netifs.sort(key=lambda x: x.get("bytes_sent"), reverse=True)

    data = {
        "os": platform.platform().decode("utf-8"),
        "hostname": socket.gethostname().decode("utf-8"),
        "uptime": str(uptime).split(".")[0],
        "load_avg": load_avg,
        "cpus": psutil.NUM_CPUS,
        "vmem": psutil.virtual_memory(),
        "swap": psutil.swap_memory(),
        "disks": disks,
        "cpu_percent": psutil.cpu_times_percent(0),
        "users": users,
        "net_interfaces": netifs,
        "page": "overview",
        "is_xhr": request.is_xhr
    }

    return render_template("index.html", **data)


@psdashapp.route("/processes", defaults={"sort": "cpu", "order": "desc"})
@psdashapp.route("/processes/<string:sort>")
@psdashapp.route("/processes/<string:sort>/<string:order>")
def processes(sort="pid", order="asc"):
    procs = []
    for p in psutil.process_iter():
        rss, vms = p.get_memory_info()

        # format created date from unix-timestamp
        dt = datetime.fromtimestamp(p.create_time)
        created = dt.strftime("%Y-%m-%d %H:%M:%S")

        proc = {
            "pid": p.pid,
            "name": p.name.decode("utf-8"),
            "cmdline": u" ".join(arg.decode("utf-8") for arg in p.cmdline),
            "username": p.username.decode("utf-8"),
            "status": p.status,
            "created": created,
            "rss": rss,
            "vms": vms,
            "memory": p.get_memory_percent(),
            "cpu": p.get_cpu_percent(0)
        }

        procs.append(proc)

    procs.sort(
        key=lambda x: x.get(sort),
        reverse=True if order != "asc" else False
    )

    return render_template(
        "processes.html",
        processes=procs,
        sort=sort,
        order=order,
        page="processes",
        is_xhr=request.is_xhr
    )


@psdashapp.route("/process/<int:pid>/limits")
def process_limits(pid):
    p = psutil.Process(pid)

    limits = {
        "RLIMIT_AS": p.get_rlimit(psutil.RLIMIT_AS),
        "RLIMIT_CORE": p.get_rlimit(psutil.RLIMIT_CORE),
        "RLIMIT_CPU": p.get_rlimit(psutil.RLIMIT_CPU),
        "RLIMIT_DATA": p.get_rlimit(psutil.RLIMIT_DATA),
        "RLIMIT_FSIZE": p.get_rlimit(psutil.RLIMIT_FSIZE),
        "RLIMIT_LOCKS": p.get_rlimit(psutil.RLIMIT_LOCKS),
        "RLIMIT_MEMLOCK": p.get_rlimit(psutil.RLIMIT_MEMLOCK),
        "RLIMIT_MSGQUEUE": p.get_rlimit(psutil.RLIMIT_MSGQUEUE),
        "RLIMIT_NICE": p.get_rlimit(psutil.RLIMIT_NICE),
        "RLIMIT_NOFILE": p.get_rlimit(psutil.RLIMIT_NOFILE),
        "RLIMIT_NPROC": p.get_rlimit(psutil.RLIMIT_NPROC),
        "RLIMIT_RSS": p.get_rlimit(psutil.RLIMIT_RSS),
        "RLIMIT_RTPRIO": p.get_rlimit(psutil.RLIMIT_RTPRIO),
        "RLIMIT_RTTIME": p.get_rlimit(psutil.RLIMIT_RTTIME),
        "RLIMIT_SIGPENDING": p.get_rlimit(psutil.RLIMIT_SIGPENDING),
        "RLIMIT_STACK": p.get_rlimit(psutil.RLIMIT_STACK)
    }

    return render_template(
        "process/limits.html",
        limits=limits,
        process=p,
        section="limits",
        page="processes",
        is_xhr=request.is_xhr
    )


@psdashapp.route("/process/<int:pid>", defaults={"section": "overview"})
@psdashapp.route("/process/<int:pid>/<string:section>")
def process(pid, section):
    valid_sections = [
        "overview",
        "threads",
        "files",
        "connections",
        "memory",
        "children"
    ]

    if section not in valid_sections:
        errmsg = "Invalid subsection when trying to view process %d" % pid
        return render_template("error.html", error=errmsg), 404

    return render_template(
        "process/%s.html" % section,
        process=psutil.Process(pid),
        section=section,
        page="processes",
        is_xhr=request.is_xhr
    )


@psdashapp.route("/network")
def view_networks():
    netifs = get_network_interfaces()
    netifs.sort(key=lambda x: x.get("bytes_sent"), reverse=True)
    return render_template(
        "network.html",
        page="network",
        network_interfaces=netifs,
        is_xhr=request.is_xhr
    )


@psdashapp.route("/disks")
def view_disks():
    disks = get_disks(all_partitions=True)
    io_counters = psutil.disk_io_counters(perdisk=True).items()
    io_counters.sort(key=lambda x: x[1].read_count, reverse=True)
    return render_template(
        "disks.html",
        page="disks",
        disks=disks,
        io_counters=io_counters,
        is_xhr=request.is_xhr
    )


@psdashapp.route("/logs")
def view_logs():
    available_logs = []
    for log in logs.get_available():
        try:
            stat = os.stat(log.filename)
        except OSError:
            logger.warning("Could not stat %s, removing from available logs", log.filename)
            logs.remove_available(log.filename)
            continue

        dt = datetime.fromtimestamp(stat.st_atime)
        last_access = dt.strftime("%Y-%m-%d %H:%M:%S")

        dt = datetime.fromtimestamp(stat.st_mtime)
        last_modification = dt.strftime("%Y-%m-%d %H:%M:%S")

        available_logs.append({
            "filename": log.filename,
            "size": stat.st_size,
            "last_access": last_access,
            "last_modification": last_modification
        })

    available_logs.sort(cmp=lambda x1, x2: locale.strcoll(x1["filename"], x2["filename"]))

    return render_template(
        "logs.html",
        page="logs",
        logs=available_logs,
        is_xhr=request.is_xhr
    )


@psdashapp.route("/log")
def view_log():
    filename = request.args["filename"]

    try:
        log = logs.get(filename, key=session.get("client_id"))
        log.set_tail_position()
        content = log.read()
        print(log.fp.tell())
    except KeyError:
        return render_template("error.html", error="Only files passed through args are allowed."), 401

    return render_template("log.html", content=content, filename=filename)


@psdashapp.route("/log/read")
def read_log():
    filename = request.args["filename"]

    try:
        log = logs.get(filename, key=session.get("client_id"))
        return log.read()
    except KeyError:
        return "Could not find log file with given filename", 404


@psdashapp.route("/log/read_tail")
def read_log_tail():
    filename = request.args["filename"]

    try:
        log = logs.get(filename, key=session.get("client_id"))
        log.set_tail_position()
        return log.read()
    except KeyError:
        return "Could not find log file with given filename", 404


@psdashapp.route("/log/search")
def search_log():
    filename = request.args["filename"]
    query_text = request.args["text"]

    log = logs.get(filename, key=session.get("client_id"))
    pos, bufferpos, res = log.search(query_text)
    if log.searcher.reached_end():
        log.searcher.reset()

    stat = os.stat(log.filename)

    data = {
        "position": pos,
        "buffer_pos": bufferpos,
        "filesize": stat.st_size,
        "content": res
    }

    return jsonify(data)


def parse_args():
    parser = argparse.ArgumentParser(
        description="psdash %s - system information web dashboard" % "0.3.0"
    )
    parser.add_argument(
        "-l", "--log",
        action="append",
        dest="logs",
        default=[],
        metavar="path",
        help="log files to make available for psdash. Patterns (e.g. /var/log/**/*.log) are supported. "
             "This option can be used multiple times."
    )
    parser.add_argument(
        "-b", "--bind",
        action="store",
        dest="bind_host",
        default="0.0.0.0",
        metavar="host",
        help="host to bind to. Defaults to 0.0.0.0 (all interfaces)."
    )
    parser.add_argument(
        "-p", "--port",
        action="store",
        type=int,
        dest="port",
        default=5000,
        metavar="port",
        help="port to listen on. Defaults to 5000."
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        dest="debug",
        help="enables debug mode."
    )

    return parser.parse_args()


def start_background_worker(args, sleep_time=3):
    def work():
        update_logs_interval = 60
        i = update_logs_interval
        while True:
            net_io_counters.update()

            # update the list of available logs every minute
            if update_logs_interval <= 0:
                logs.add_patterns(args.logs)
                i = update_logs_interval
            i -= sleep_time

            time.sleep(sleep_time)

    t = threading.Thread(target=work)
    t.daemon = True
    t.start()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(name)s | %(message)s"
    )

    logging.getLogger("werkzeug").setLevel(logging.WARNING)


def enable_verbose_logging():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("werkzeug").setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)


def main():
    setup_logging()

    logger.info("Starting psdash v0.3.0")

    # This set locale to the user default (usually controlled by the LANG env var)
    locale.setlocale(locale.LC_ALL, "")

    args = parse_args()
    if args.debug:
        enable_verbose_logging()

    logs.add_patterns(args.logs)
    start_background_worker(args)

    logger.info("Listening on %s:%s", args.bind_host, args.port)

    app.register_blueprint(psdashapp)

    app.run(
        host=args.bind_host,
        port=args.port,
        debug=args.debug,
        threaded=True
    )


if __name__ == '__main__':
    main()

########NEW FILE########
__FILENAME__ = log_test
import os
import tempfile
import unittest
from psdash.log import Logs, LogReader


class TestLogs(unittest.TestCase):
    NEEDLE = "foobar\n"
    POSITIONS = [10000, 8000, 6000, 4000, 2000, 500]

    def setUp(self):
        fd, filename = tempfile.mkstemp()
        self.filename = filename
        self.fp = os.fdopen(fd, "w+")
        for pos in self.POSITIONS:
            self.fp.seek(pos)
            self.fp.write(self.NEEDLE)
        self.fp.close()
        self.logs = Logs()
        self.logs.add_available(filename)

    def tearDown(self):
        os.remove(self.filename)
        self.logs.clear_available()

    def test_searching(self):
        log = self.logs.get(self.filename)
        log.searcher.reset()
        positions = [log.search(self.NEEDLE)[0] for _ in xrange(len(self.POSITIONS))]
        self.assertEqual(self.POSITIONS, positions)

    def test_searching_other_buffer_size(self):
        log = LogReader(self.filename, LogReader.BUFFER_SIZE / 2)
        log.searcher.reset()
        positions = [log.search(self.NEEDLE)[0] for _ in xrange(len(self.POSITIONS))]
        self.assertEqual(self.POSITIONS, positions)


if __name__ == "__main__":
    unittest.main()
########NEW FILE########