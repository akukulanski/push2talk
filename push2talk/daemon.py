import sys, os, time, atexit
from signal import SIGTERM
from abc import ABCMeta, abstractmethod

def _read_pid(filename):
    try:
        with open(filename, 'r') as f:
            pid = int(f.read().strip())
    except IOError:
        pid = None
    return pid

class Daemon(metaclass=ABCMeta):
    """
    A generic daemon class.
   
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(f'fork #1 failed: {e.errno} ({e.strerror})\n')
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(f'fork #2 failed: {e.errno} {e.stderr}\n')
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')# se = open(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(f'{pid}\n')
   
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        # Check for a pidfile to see if the daemon already runs
        pid = _read_pid(self.pidfile)

        if pid:
            sys.stderr.write(f'pidfile {self.pidfile} already exist. '
                             f'Daemon already running?\n')
            sys.exit(1)
   
        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        # Get the pid from the pidfile
        pid = _read_pid(self.pidfile)

        if not pid:
            sys.stderr.write(
                    f'pidfile {self.pidfile} does not exist. '
                    f'Daemon not running?\n')
            return # not an error in a restart

        # Try killing the daemon process       
        try:
            while True:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    self.delpid()
            else:
                print(str(err))
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def is_running(self):
        pid = _read_pid(self.pidfile)
        return bool(pid)

    @abstractmethod
    def run(self):
        pass
