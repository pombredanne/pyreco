__FILENAME__ = test_bind
import unittest
import subprocess
import sys
import os
import re
import random

def _f(x):
    return os.path.join(os.path.dirname(__file__), x)

class NonZeroExit(Exception):
    pass

class RegexEqual(object):
    def __init__(self, r):
        self.re = re.compile(r)
    
    def __eq__(self, x):
        return bool(self.re.search(x))

class BindTest(unittest.TestCase):
    def setUp(self):
        self._cmd('create', self.zone)
            
    def tearDown(self):
        # clear up
        self._cmd('rrpurge', '--confirm', self.zone)
        self._cmd('delete', self.zone)
        
    def _zonefile(self, fname):
        with file('temp.txt', 'w') as fout:
            print >>fout, "$ORIGIN %s." % self.zone
            with file(_f(fname), 'r') as fin:
                fout.write(fin.read())
        return 'temp.txt'
        
    def _cmd(self, cmd, *args):
        pargs = ('scripts/cli53', cmd) + args
        p = subprocess.Popen(pargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        if p.returncode:
            # print >> sys.stderr, p.stderr.read()
            raise NonZeroExit
        return p.stdout.read()
        
class ZoneTest(BindTest):
    zone = '%d.example.com' % random.randint(0, sys.maxint)

    def test_import(self):
        fname = self._zonefile('zone1.txt')
        self._cmd('import', '--file', fname, self.zone)
        
        output = self._cmd('export', self.zone)
        output = [ x for x in output.split('\n') if x ]
        output.sort()
        
        self.assertEqual(
            [
                "$ORIGIN %s." % self.zone,
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                "@ 86400 IN A 10.0.0.1",
                "@ 86400 IN MX 10 mail.example.com.",
                "@ 86400 IN MX 20 mail2.example.com.",
                "@ 86400 IN TXT \"v=spf1 a mx a:cli53.example.com mx:mail.example.com ip4:10.0.0.0/24 ~all\"",
                RegexEqual('^@ 900 IN SOA'),
                "mail 86400 IN A 10.0.0.2",
                "mail2 86400 IN A 10.0.0.3",
                'test 86400 IN TXT "multivalued" " txt \\"quoted\\" record"',
                "www 86400 IN A 10.0.0.1",
            ],
            output
        )

    def test_import2(self):
        fname = self._zonefile('zone2.txt')
        self._cmd('import', '--file', fname, self.zone)
        
        output = self._cmd('export', self.zone)
        output = [ x for x in output.split('\n') if x ]
        output.sort()
        
        self.assertEqual(
            [
                "$ORIGIN %s." % self.zone,
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                "@ 86400 IN A 10.0.0.1",
                "@ 86400 IN MX 10 mail.example.com.",
                "@ 86400 IN MX 20 mail2.example.com.",
                "@ 86400 IN TXT \"v=spf1 a mx a:cli53.example.com mx:mail.example.com ip4:10.0.0.0/24 ~all\"",
                RegexEqual('^@ 900 IN SOA'),
                "mail 86400 IN A 10.0.0.2",
                "mail2 86400 IN A 10.0.0.3",
                'test 86400 IN TXT "multivalued" " txt \\"quoted\\" record"',
                "www 86400 IN A 10.0.0.1",
            ],
            output
        )

    def disabled_aws_extensions(self):
        # disabled - they require a valid ELB to point to
        fname = self._zonefile('zoneaws.txt')
        self._cmd('import', '--file', fname, self.zone)
        
        output = self._cmd('export', self.zone)
        output = [ x for x in output.split('\n') if x ]
        output.sort()
        
        self.assertEqual(
            [
                "$ORIGIN %s." % self.zone,
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 900 IN SOA'),
                "test 86400 AWS A 10 127.0.0.1 abc",
                "test 86400 AWS A 20 127.0.0.2 def",
                "test2 600 AWS ALIAS Z3NF1Z3NOM5OY2 test-212960849.eu-west-1.elb.amazonaws.com.",
                "test3 600 AWS ALIAS region:us-west-1 Z3NF1Z3NOM5OY2 test-212960849.eu-west-1.elb.amazonaws.com. identifier-test-id",
                "test4 600 AWS ALIAS 50 Z3NF1Z3NOM5OY2 test-212960849.eu-west-1.elb.amazonaws.com. latency-test-id",
            ],
            output
        )

    def test_invalid1(self):
        fname = self._zonefile('invalid1.txt')
        self.assertRaises(NonZeroExit,
            self._cmd, 'import', '--file', fname, self.zone)

def random_arpa_address():
    p = tuple(random.randint(0, 255) for x in range(3))
    return '0/%d.%d.%d.10.in-addr.arpa' % p

class ArpaTest(BindTest):
    zone = random_arpa_address()

    def test_import_arpa(self):
        fname = self._zonefile('zone3.txt')
        self._cmd('import', '--file', fname, self.zone)
        
        output = self._cmd('export', self.zone)
        output = [ x for x in output.split('\n') if x ]
        output.sort()
        
        self.assertEqual(
            [
                "$ORIGIN %s." % self.zone,
                "98 0 IN PTR blah.foo.com.",
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 172800 IN NS'),
                RegexEqual('^@ 900 IN SOA'),
            ],
            output
        )

########NEW FILE########
__FILENAME__ = test_commands
import unittest
import subprocess
import sys
import re
import random

class NonZeroExit(Exception):
    pass

class RegexEqual(object):
    def __init__(self, r):
        self.re = re.compile(r)
    
    def __eq__(self, x):
        return bool(self.re.search(x))

class CommandsTest(unittest.TestCase):
    def setUp(self):
        # re-use if already created
        self.zone = '%d.example.com' % random.randint(0, sys.maxint)
        self._cmd('create', self.zone, '--comment', 'unittests')
            
    def tearDown(self):
        # clear up
        self._cmd('rrpurge', '--confirm', self.zone)
        self._cmd('delete', self.zone)
        
    def _cmd(self, cmd, *args):
        pargs = ('scripts/cli53', cmd) + args
        p = subprocess.Popen(pargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        if p.returncode:
            print >> sys.stderr, p.stderr.read()
            raise NonZeroExit
        return p.stdout.read()
        
    def test_rrcreate(self):
        self._cmd('rrcreate', self.zone, '', 'A', '10.0.0.1')
        self._cmd('rrcreate', self.zone, 'www', 'CNAME', self.zone+'.', '-x 3600')
        self._cmd('rrcreate', self.zone, 'info', 'TXT', 'this is a "test"')
        self._cmd('rrcreate', self.zone, 'weighttest1', 'CNAME', self.zone+'.', '-x 60', '-w 0', '-i awsweightzero')
        self._cmd('rrcreate', self.zone, 'weighttest2', 'CNAME', self.zone+'.', '-x 60', '-w 1', '-i awsweightone')
        self._cmd('rrcreate', self.zone, 'weighttest3', 'CNAME', self.zone+'.', '-x 60', '-w 50', '-i awsweightfifty')

        output = self._cmd('export', self.zone)
        output = [ x for x in output.split('\n') if '10.0.0.1' in x or 'CNAME' in x or 'TXT' in x ]

        self.assertEqual(
            [
                "@ 86400 IN A 10.0.0.1",
                'info 86400 IN TXT "this is a \\"test\\""',
                "weighttest1 60 AWS CNAME 0 %s.  awsweightzero" % self.zone,
                "weighttest2 60 AWS CNAME 1 %s.  awsweightone" % self.zone,
                "weighttest3 60 AWS CNAME 50 %s.  awsweightfifty" % self.zone,
                "www 3600 IN CNAME %s." % self.zone,
            ],
            output
        )

    def test_rrdelete(self):
        self._cmd('rrcreate', self.zone, '', 'A', '10.0.0.1')
        self._cmd('rrdelete', self.zone, '', 'A')
        
    def test_rrcreate_replace_latency(self):
        self._cmd('rrcreate', '-i', 'asiacdn', '--region', 'ap-southeast-1', self.zone, 'cdn', 'CNAME', 'asiacdn.com.')
        self._cmd('rrcreate', '-i', 'statescdn', '--region', 'us-west-1', self.zone, 'cdn', 'CNAME', 'uscdn.com.')
        self._cmd('rrcreate', '-i', 'newuscdn', '--region', 'us-west-1', self.zone, 'cdn', 'CNAME', 'newuscdn.com.', '-r')

########NEW FILE########
__FILENAME__ = test_domains
import sys
import unittest
import subprocess
import random

# copied from python 2.7 for python 2.6
def check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd, output=output)
    return output

class DomainsTest(unittest.TestCase):
    def _cmd(self, cmd, *args):
        pargs = ('scripts/cli53', cmd) + args
        return check_output(pargs, stderr=subprocess.STDOUT)
        
    def _unique_name(self):
        return 'temp%d.com' % random.randint(0, sys.maxint)
        
    def test_usage(self):
        assert 'usage' in self._cmd('-h')        

    def test_create_delete(self):
        name = self._unique_name()
        self._cmd('create', name)
        assert name in self._cmd('list')
        self._cmd('delete', name)
        assert name not in self._cmd('list')

########NEW FILE########