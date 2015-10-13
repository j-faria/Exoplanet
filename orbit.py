import numpy as np 

class Orbit():
	def __init__(self, filename):
		self.vx, self.vy = np.loadtxt(filename, unpack=True)

	def evaluate(self, arg_to_cos, viewing_angle):
		# Create radial velocities
		C = np.cos(viewing_angle)
		S = np.sin(viewing_angle)
		vr = self.vx
		vrmax = -1E300
		vrmin =  1E300
		highest = 0

		for i in range(len(vr)):
			vr[i] = C*self.vx[i] + S*self.vy[i]
			if (vr[i] > vrmax):
				vrmax = vr[i]
			if (vr[i] < vrmin):
				vrmin = vr[i]
			if (vr[i] > vr[highest]):
				highest = i


		for i in range(len(vr)):
			vr[i] = 2.*(vr[i] - vrmin)/(vrmax - vrmin) - 1.

		result = arg_to_cos
		cc = 2.*np.pi*float(highest) / vr.size

		for i in range(len(result)):
			index = int((vr.size * np.mod(arg_to_cos[i] + cc, 2.*np.pi) / (2*np.pi) ))
			result[i] = vr[index]

		self.result = result
		return result


def test_Orbit():
	o = Orbit('Orbits/orbits0.710.dat')


	t = np.arange(-10, 10, 0.01)

	y = o.evaluate(t, 1.)

	for tt, yy in zip(t[:10], y[:10]):
		print tt, yy, tt==yy