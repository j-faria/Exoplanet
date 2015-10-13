import numpy as np 
from glob import glob
import cPickle
import os
from orbit import Orbit

class Lookup():
	def __init__(self, cache=True):
		self.orbit_files = sorted(glob('Orbits/orbits*.dat'))

		cached_file = 'LookupOrbits.pickle'
		if os.path.exists(cached_file) and cache:
			orbits = cPickle.load(open(cached_file))
			print "# Loaded orbit cached file"
		else:
			orbits = np.empty_like(self.orbit_files, dtype=object)
			for i, f in enumerate(self.orbit_files):
				# print f
				orbits[i] = Orbit(f)

			print "# Loaded orbit files"
			self.cache(orbits)

		self.orbits = orbits

	def evaluate(self, arg_to_sin, v0, viewing_angle):
		# If v0 is out of bounds, do nothing
		if (v0 < 0.4 and v0 > 1.):
			return None

		which = (v0 - 0.4)/0.005
		return self.orbits[which].evaluate(arg_to_sin, viewing_angle)

	def cache(self, obj):
		""" Caching this saves about 2 seconds. """
		cPickle.dump(obj, open('LookupOrbits.pickle', 'w'))

if __name__ == '__main__':
	l = Lookup()