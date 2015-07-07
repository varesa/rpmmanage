#!/usr/bin/env python

"""asyncsubproc.py: Asynchronous subprocess communication using asyncore.

Wraps the input, output, and error pipes from a Subprocess.Popen() object
in asyncore.file_dispatcher() objects, allowing asynchronous communication
with the subprocess.

In addition, overrides the asyncore.loop() function to check for exited
subprocesses. [This means, however, that it *only* checks for exits every
time asyncore.loop() loops around, so the the timeout value passed to
loop() is also time resolution of detecting process exits.]

References:
http://code.activestate.com/recipes/440554/
http://code.activestate.com/recipes/576759/
http://parijatmishra.blogspot.com/2008/01/writing-server-with-pythons-asyncore.html
"""

import errno
import os
import time
import asyncore
from subprocess import Popen, PIPE
from asyncore import file_dispatcher

process_map = {}


class StdioHandler(file_dispatcher):
    """Generic routines for asynchronous I/O pipe handlers.

    Can also be used with Popen.communicate(), since the important file
    object methods are delegated.
    """

    def __init__(self, fh, subproc, map=None, maxdata=512):
        self.subproc = subproc
        self.maxdata = maxdata
        self.__filehandle = fh
        file_dispatcher.__init__(self, os.dup(fh.fileno()), map=map)

    def flush(self):
        """Delegate to the original file handle."""
        if self.__filehandle:
            return self.__filehandle.flush()
        else:
            raise EOFError('Pipe closed.')

    def read(self, *args):
        """Delegate to the original file handle."""
        if self.__filehandle:
            return self.__filehandle.read(*args)
        else:
            raise EOFError('Pipe closed.')

    def write(self, *args):
        """Delegate to the original file handle."""
        if self.__filehandle:
            return self.__filehandle.write(*args)
        else:
            raise EOFError('Pipe closed.')

    def fileno(self):
        """Delegate to the original file handle."""
        if self.__filehandle:
            return self.__filehandle.fileno()
        else:
            raise EOFError('Pipe closed.')

    def readable(self):
        """Returns true if the pipe is still open."""
        return self.__filehandle is not None

    def writable(self):
        """Returns true if the pipe is still open."""
        return self.__filehandle is not None

    def send(self, buffer):
        """Wrapper which checks for closed and broken pipes.
        
        Occasionally, the handler may try to write to a broken pipe if the
        subprocess exited unexpectedly.  (SIG* happens.)  When this occurs,
        calls handle_expt()."""
        if self.__filehandle:
            try:
                return file_dispatcher.send(self, buffer)
            except OSError as oe:
                self.handle_expt()
                if oe.errno not in [errno.EPIPE, errno.EBADF]:
                    raise oe
        return 0

    def recv(self, buffer_size):
        """Wrapper which checks for closed and broken pipes.
        
        Occasionally, the handler may try to read from a broken pipe if the
        subprocess exited unexpectedly.  (SIG* happens.)  When this occurs,
        calls handle_expt()."""
        if self.__filehandle:
            try:
                return file_dispatcher.recv(self, buffer_size)
            except OSError as oe:
                self.handle_expt()
                if oe.errno not in [errno.EPIPE, errno.EBADF]:
                    raise oe
        return ''

    def handle_close(self):
        """Closes the pipe and calls the AsyncPopen object callback."""
        if self.__filehandle:
            # Occasionally the handler will try to close a broken pipe if the
            # subprocess exited unexpectedly.  (SIG* happens.)  Catch and ignore.
            try:
                try:
                    self.close()
                except OSError as oe:
                    if oe.errno not in [errno.EPIPE, errno.EBADF]:
                        raise oe
                try:
                    self.__filehandle.close()
                except OSError as oe:
                    if oe.errno not in [errno.EPIPE, errno.EBADF]:
                        raise oe
            finally:
                self.__filehandle = None
                self.subproc.call_closed_callback(self)

    def handle_expt(self):
        """Calls handle_close() to close the pipe.  It's all the handler can
        do without more info."""
        self.handle_close()


class StdInputHandler(StdioHandler):
    """Push data to a stdin pipe using asyncore."""

    def __init__(self, fh, subproc, map=None, maxdata=512):
        self.__buffer = None
        self.__offset = 0
        StdioHandler.__init__(self, fh, subproc, map=map, maxdata=maxdata)

    def readable(self):
        """Subprocess stdin is never readable."""
        return False

    def writable(self):
        """If data is in the buffer and the pipe is open, return True."""
        return StdioHandler.writable(self) and (self.__buffer is not None)

    def push_data(self, data):
        """Push some data by putting it in the output buffer.  Raises an
        EOFError if the pipe is already closed."""
        if not StdioHandler.writable(self):
            raise EOFError('Input pipe closed.')
        elif self.__buffer:
            # Since we have to construct a new string, remove the already-sent data.
            self.__buffer = self.__buffer[self.__offset:] + data
        else:
            self.__buffer = data
        self.__offset = 0

    def handle_write(self):
        """Write up to maxdata bytes from the buffer.  The default for maxdata
        is 512, because that's all POSIX guarantees."""
        if self.writable():
            self.__offset += self.send(
                self.__buffer[self.__offset:self.__offset + self.maxdata])
            # If the buffer is all written, empty it.
            if self.__offset >= len(self.__buffer):
                self.__buffer = None
                self.__offset = 0


class StdOutputHandler(StdioHandler):
    """Get data from a stdout/stderr pipe using asyncore."""

    def __init__(self, fh, subproc, map=None, maxdata=1024):
        self.__data = []
        self.__endedcr = False
        StdioHandler.__init__(self, fh, subproc, map=map, maxdata=maxdata)

    def writable(self):
        """Subprocess stdout/stderr is never writable."""
        return False

    def handle_read(self):
        """Read up to maxdata bytes, queue the data, and call the callback."""
        if self.readable():
            data = self.recv(self.maxdata)
            if data:
                self.__data.append(data.decode())
                self.subproc.call_new_data_callback(self)

    def fetch_data(self):
        """Return all the accumulated data from the pipe as a string,
        and clear the accumulated data."""
        if self.__data:
            datastr = ''.join(self.__data)
            self.__data[:] = []
            if self.subproc.universal_newlines and datastr:
                # Take care of a newline split across reads.
                stripnl = self.__endedcr
                self.__endedcr = (datastr[-1] == '\r')
                if stripnl and datastr[0] == '\n':
                    return self.subproc._translate_newlines(datastr[1:])
                else:
                    return self.subproc._translate_newlines(datastr)
            else:
                return datastr
        else:
            return ''


class AsyncPopen(Popen):
    """Extend Popen to provide asynchronous communication through asyncore.
    
    *Warning* about bidirectional communication: data that the subprocess
    writes to stdout/stderr might not be made available to the parent until
    the subprocess calls flush() or exits.  This means that a parent
    process which implements expect-like behavior (e.g. by writing to stdin
    from the stdout_new_data() callback) might find itself deadlocked.
    
    There may be some way to fix this, but I haven't found it (at least in
    Mac OS X). Changing the value of bufsize in Popen() doesn't fix it, and
    asyncore.file_dispatcher already calls fcntl() to set the O_NONBLOCK
    flag on the pipes.
    """

    def __init__(self, args, map=None, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                 callback=None, maxwrite=512, maxread=1024, **keywmap):
        """Init the subprocess object, wrapping the standard I/O pipes in
        dispatchers.  Note that the defaults are changed to PIPE for all I/O."""
        if map is None:
            self._map = process_map
        else:
            self._map = map
        self.__callback = callback
        Popen.__init__(self, args, stdin=stdin, stdout=stdout, stderr=stderr, **keywmap)
        self.add_subprocess(map)
        if self.stdin:
            self.stdin = StdInputHandler(self.stdin, self, maxdata=maxwrite)
        if self.stdout:
            self.stdout = StdOutputHandler(self.stdout, self, maxdata=maxread)
        if self.stderr:
            self.stderr = StdOutputHandler(self.stderr, self, maxdata=maxread)

    def add_subprocess(self, map=None):
        if map is None:
            map = self._map
        map[self.pid] = self

    def del_subprocess(self, map=None):
        if map is None:
            map = self._map
        if self.pid in map:
            del map[self.pid]

    def check_exit(self):
        """Check if the subprocess has finished and all the output pipes are
        empty.  If so, really close the pipes and call the exit callback."""
        exitstat = self.poll()
        if (exitstat is None) or (
                    self.stdout and self.stdout.readable()) or (
                    self.stderr and self.stderr.readable()):
            return False
        if self.stdin:
            self.stdin.handle_close()
        self.__call_callback('exited', self)
        self.del_subprocess()

    def call_new_data_callback(self, dispatcher):
        """Call a method of the callback object to signal new data."""
        self.__call_callback('new_data', dispatcher)

    def call_closed_callback(self, dispatcher):
        """Call a method of the callback object to signal pipe closed."""
        self.__call_callback('closed', dispatcher)

    def __call_callback(self, callback_name, dispatcher):
        """Call a method of the callback object to signal an event.
        
        Does *not* trap exceptions in the callback (though maybe it should),
        because there is nothing useful that can be done with them.  (Maybe
        the callback object needs an error logging method?)
        """
        if not self.__callback:
            return
        # Figure out which dispatcher this is and add it to the method name
        if dispatcher is self.stdout:
            callback_name = 'stdout_' + callback_name
        elif dispatcher is self.stderr:
            callback_name = 'stderr_' + callback_name
        elif dispatcher is self.stdin:
            callback_name = 'stdin_' + callback_name
        elif dispatcher is self:
            callback_name = 'subprocess_' + callback_name
        else:
            return
        # If the method exists, call it
        if hasattr(self.__callback, callback_name):
            method = getattr(self.__callback, callback_name)
            method(self)


class AsyncPopenCallbackDemo:
    """A callback object, showing the methods that can be implemented.  Not
    all callback methods must be implemented; they are checked dynamically.
    
    The callback methods receive the Popen object so that they have full
    control of the subprocess and can kill() it, or send new data to
    stdin when data is received on stdout or stderr.  See the warning in
    AsyncPopen about bidirectional communication, however!
    """

    def __init__(self, errlast=False, unitlen=10):
        self.__errlast = errlast
        self.__unitlen = unitlen

    def __stdout_get_data(self, popen_obj):
        data = popen_obj.stdout.fetch_data()
        if hasattr(popen_obj, 'stdout_data_received'):
            popen_obj.stdout_data_received += len(data)
        else:
            popen_obj.stdout_data_received = len(data)
        self.printdata(data, popen_obj.stdout_data_received, popen_obj.pid, 'stdout')
        return data

    def __stderr_get_data(self, popen_obj):
        data = popen_obj.stderr.fetch_data()
        if hasattr(popen_obj, 'stderr_data_received'):
            popen_obj.stderr_data_received += len(data)
        else:
            popen_obj.stderr_data_received = len(data)
        self.printdata(data, popen_obj.stderr_data_received, popen_obj.pid, 'stderr')
        return data

    def stdout_new_data(self, popen_obj):
        """Called when data is received on stdout.  Data can be read by
        calling popen_obj.stdout.fetch_data()"""
        data = self.__stdout_get_data(popen_obj)
        if data:
            # We might find a closed pipe when we try to write.
            try:
                popen_obj.stdin.push_data(data)
            except EOFError:
                pass

    def stderr_new_data(self, popen_obj):
        """Called when data is received on stderr.  Data can be read by
        calling popen_obj.stderr.fetch_data()"""
        if not self.__errlast:
            self.__stderr_get_data(popen_obj)

    def stdin_closed(self, popen_obj):
        """Called when stdin is closed."""
        self.printmsg('closed', popen_obj.pid, 'stdin')

    def stdout_closed(self, popen_obj):
        """Called when stdout is closed.  Remaining data can be read
        by calling popen_obj.stdout.fetch_data()"""
        self.printmsg('closed', popen_obj.pid, 'stdout')
        self.__stdout_get_data(popen_obj)

    def stderr_closed(self, popen_obj):
        """Called when stderr is closed.  Remaining data can be read
        by calling popen_obj.stderr.fetch_data()"""
        self.printmsg('closed', popen_obj.pid, 'stderr')
        if not self.__errlast:
            self.__stderr_get_data(popen_obj)

    def subprocess_exited(self, popen_obj):
        """Called when the subprocess is found to have exited."""
        self.printmsg('subprocess exited with %d' % popen_obj.returncode, popen_obj.pid, 'exit')
        self.__stdout_get_data(popen_obj)
        self.__stderr_get_data(popen_obj)

    def printdata(self, data, total_bytes, pid, channame):
        if not data:
            printable = ''
        else:
            printable = ': ' + repr(data)
        self.printmsg('%d/%d bytes received%s' % (len(data),
                                                  total_bytes, printable), pid, channame)

    def printmsg(self, msg, pid, channame):
        print('[%d] %s: %s' % (pid, channame, msg))

# Hijack the asyncore loop to add process exit checking
__asyncore_loop = asyncore.loop


def __loop(timeout=1.0, map=None, procmap=None, count=None, **keywmap):
    if map is None:
        map = asyncore.socket_map
    if procmap is None:
        procmap = process_map

    checkproc = True
    while (map or procmap) and (count is None or count > 0):
        if checkproc and procmap:
            for pid, popen in procmap.items():
                popen.check_exit()
        elif map:
            __asyncore_loop(timeout=timeout, map=map, count=1, **keywmap)
        else:
            time.sleep(timeout)
        checkproc = not checkproc
        if count is not None: count -= 1


asyncore.loop = __loop

if __name__ == "!__main__":
    callback = AsyncPopenCallbackDemo()
    subprocs = [AsyncPopen(['find', '/'], callback=callback)]
    for p in subprocs:
        asyncore.loop(1)
