mocksey
=======

Stupidly-simple python mocking utility with moxie.

|BuildImage|_

.. image:: https://pypip.in/v/mocksey/badge.png
    :target: https://crate.io/packages/mocksey/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/mocksey/badge.png
    :target: https://crate.io/packages/mocksey/
    :alt: Number of PyPI downloads

|Coverage Status|

 .. |Coverage Status| image:: https://coveralls.io/repos/mitgr81/mocksey/badge.png
    :target: https://coveralls.io/r/mitgr81/mocksey


Mocksey Motivation
==================

I was teaching a class on unit testing to a group of co-workers who were familiar with `Simple Test for PHP <http://www.simpletest.org/>`_ so I hacked together what is becoming Mocksey.

Mocksey the TDD'd version of that TDD utilty. `It's so meta even this acronym <http://xkcd.com/917/>`_.

Installation
============

Either find mocksey on PyPI_ or install it with pip or easy_install
::

  pip install mocksey
  #or
  easy_install mocksey

Basic Usage
===========

It's pretty simple.  Create a mocked object with generate_mock, inject it (or monkey patch) and set up your assertions.  After your function call(s), simply call 'run_asserts' and win!

The unit tests are a pretty decent working example.

Tweaksey
========

Tweaksey is a collection of beautification wrappers.  Currently there's only one around mock_, but there may be more in the future.  It'll look best if you also have nose_ installed, and may only be worth it in that case, actually.  Anyhow, to use it simply import tweaksey from mocksey and get your copy of the mock package from ``tweaksey.tweak_mock``.  Your mock assertions should now have a touch more friendliness.  If there are more you'd like to add, go for it!  Michael Foord, if you want to take the output and run, that cool too (conversely, if you don't like that I did this, I'll kill it square dead).


Changelog
=========

0.3.1
-----
Mocksey now sets nose to full diff mode.

0.3.0
-----
Tweaksey now requires you to pass in the 'mock' library that you're
tweaking.  This allows one to apply mocks to python3's ``unittest.mock``.


License
=======
This software is hereby released under the MIT License, as seen in the LICENSE file

.. |BuildImage| image:: https://secure.travis-ci.org/mitgr81/mocksey.png
.. _BuildImage: https://travis-ci.org/mitgr81/mocksey
.. _PyPI: http://pypi.python.org/pypi/mocksey
.. _mock: http://www.voidspace.org.uk/python/mock/
.. _nose: https://pypi.python.org/pypi/nose/
