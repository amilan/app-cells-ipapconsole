
Ipapconsole
-----------

Ipapconsole is an interactive Icepap client built on top of IPython.

Based on the previous IPython profile developed at Alba, it has been updated in
order to make it work with the recent versions of IPython ( > 3 )


Installation
------------
Before installing this package you will need to ensure that you have installed
the following dependencies:

- ipython
- pyIcePAP

Here at MAX IV we use our rpm packages for this installation, that's why dependencies
are not handled in the setup.py and they are in setup.cfg, but using the name of
our rpm packages.
It's up to each institute to install them in their most convenient way.

This could be improved in the future in order to simplify the process.

Once you have your dependencies installed, you can run:

```
python setup.py build
python setup.py install
```

After that, the module should be installed.

How to use it
-------------
Once it's installed you just need to type in a terminal:

```
ipapconsole
```

or use directly the ipython profile:

```
ipython --profile=ipapconsole
```
