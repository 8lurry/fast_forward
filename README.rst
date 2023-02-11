Forwarding tcp port with python
===============================

This package allows you to cascaded between as many machine(s) as you want.

Get the source code::

    $ git clone https://github.com/8lurry/fast_forward.git
    $ cd fast_forward

Forward between two local ports (creates two listening sockets and binds them)::

    $ ./ff --local --client-port 2323 --reverse-port 2424

Forward between a local listening port and a remote listening port (by default the local listening port is 22)::

    $ ./ff --remote-host 127.0.0.1 --remote-port 2424

And then you can ssh into your own machine through those forwarded ports, like::

    $ ssh -p 2323 username@localhost
