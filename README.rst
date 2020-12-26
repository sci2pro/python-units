================================================================
units
================================================================

.. image:: https://badge.fury.io/py/python-units.svg
    :target: https://badge.fury.io/py/python-units

Python library to represent numbers with units

Example:

.. code:: python

	import units as u
	print u.Unit(1, u.metre)


Upcoming features
================================================================
* Short and long units (currently only short units)

* Multipliers e.g. kilo (k), mega (M), kibi (KiB), ergs etc.

* Arbitrary units e.g. bits (b), cars etc.

Features
================================================================
* Basic units

.. code:: python

	import units as u
	from random import randint
	# ampere
	print u.Unit(randint(1, 100), u.ampere)
	# candela
	print u.Unit(randint(1, 100), u.candela)
	# kelvin
	print u.Unit(randint(1, 100), u.kelvin)
	# kilogram
	print u.Unit(randint(1, 100), u.kilogram)
	# metre
	print u.Unit(randint(1, 100), u.metre)
	# mole
	print u.Unit(randint(1, 100), u.mole)
	# second
	print u.Unit(randint(1, 100), u.second)

* Operations on units

.. code:: python

	import units as u
	from random import random
	x = u.Unit(random(), u.second)
	y = u.Unit(random(), u.ampere)
	# addition
	print x + y
	print y + x
	# subtraction
	print x - y
	print y - x
	# multiplication
	print x * y
	print y * x
	# division/true division
	print x / y
	print y / x
	# floor division
	print x // y
	print y // x
	# modulus
	print x % y
	# power
	print x ** y
	print y ** x

* Operations between scalars and units

.. code:: python

	import units as u
	from random import random
	x = u.Unit(random(), u.second)
	a = random() * 10
	# addition
	print a + y
	print y + a
	# subtraction
	print a - y
	print y - a
	# multiplication
	print a * y
	print y * a
	# division/true division
	print a / y
	print y / a
	# floor division
	print a // y
	print y // a
	# modulus
	print a % y
	# power
	print a ** y
	print y ** a

* Derived units

.. code:: python

	import units as u
	from random import random
	# hertz
	print u.Unit(random() * 10, u.hertz)
	# newton
	print u.Unit(random() * 10, u.newton)
	# pascal
	print u.Unit(random() * 10, u.pascal)
	# joule
	print u.Unit(random() * 10, u.joule)
	# watt
	print u.Unit(random() * 10, u.watt)
	# coulomb
	print u.Unit(random() * 10, u.coulomb)
	# volt
	print u.Unit(random() * 10, u.volt)
	# farad
	print u.Unit(random() * 10, u.farad)
	# ohm
	print u.Unit(random() * 10, u.ohm)
	# siemems
	print u.Unit(random() * 10, u.siemens)
	# weber
	print u.Unit(random() * 10, u.weber)
	# tesla
	print u.Unit(random() * 10, u.tesla)
	# henry
	print u.Unit(random() * 10, u.henry)
	# degree celcius
	print u.Unit(random() * 10, u.degree_celcius)
	# lumen
	print u.Unit(random() * 10, u.lumen)
	# lux
	print u.Unit(random() * 10, u.lux)
	# becquerel
	print u.Unit(random() * 10, u.becquerel)
	# gray
	print u.Unit(random() * 10, u.gray)
	# sievert
	print u.Unit(random() * 10, u.sievert)
	# katal
	print u.Unit(random() * 10, u.katal)

* Unpacking derived units

.. code:: python

	import units as u
	from random import random
	# hertz
	print u.Unit(random() * 10, u.hertz).full_units
	# newton
	print u.Unit(random() * 10, u.newton).full_units
	# pascal
	print u.Unit(random() * 10, u.pascal).full_units
	# joule
	print u.Unit(random() * 10, u.joule).full_units
	# watt
	print u.Unit(random() * 10, u.watt).full_units
	# coulomb
	print u.Unit(random() * 10, u.coulomb).full_units
	# volt
	print u.Unit(random() * 10, u.volt).full_units
	# farad
	print u.Unit(random() * 10, u.farad).full_units
	# ohm
	print u.Unit(random() * 10, u.ohm).full_units
	# siemems
	print u.Unit(random() * 10, u.siemens).full_units
	# weber
	print u.Unit(random() * 10, u.weber).full_units
	# tesla
	print u.Unit(random() * 10, u.tesla).full_units
	# henry
	print u.Unit(random() * 10, u.henry).full_units
	# degree celcius
	print u.Unit(random() * 10, u.degree_celcius).full_units
	# lumen
	print u.Unit(random() * 10, u.lumen).full_units
	# lux
	print u.Unit(random() * 10, u.lux).full_units
	# becquerel
	print u.Unit(random() * 10, u.becquerel).full_units
	# gray
	print u.Unit(random() * 10, u.gray).full_units
	# sievert
	print u.Unit(random() * 10, u.sievert).full_units
	# katal
	print u.Unit(random() * 10, u.katal).full_units

* Arbitrary derived units

.. code:: python

	import units as u
	speed = u.DerivedUnit.define('speed', metre / second)
	v = Unit(10, speed)

* Arbitrary custom units

.. code:: python

	from __future__ import division
	from units import BaseUnit

	class CommUnit(BaseUnit):
	    """Template class for communication units"""
	    def __init__(self, *args, **kwargs):
	        super(CommUnit, self).__init__(*args, **kwargs)
	        # redefine the base units
	        self.unit_dict = {
	            'b': 0,
	            's': 0,
	            'B': 0,
	        }
	    @classmethod
	    def define(cls, key, value=1):
	    	"""Constructor"""
	        obj = cls()
	        assert key in obj.unit_dict.keys()
	        assert isinstance(value, int)
	        obj.unit_dict[key] = value
	        return obj

which will be used as follows

.. code:: python

	bit = CommUnit.define('b') # define a bit as referring to the 'b' unit
	second = CommUnit.define('s') # a second is 's'
	data = Unit(32, bit)
	T = Unit(4, second)
	# data rate
	print data / T # 8.0 b·s^-1 - bits per second