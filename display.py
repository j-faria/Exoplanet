from matplotlib.pyplot import *
import numpy as np
import sys

rc("font", size=14, family="serif", serif="Computer Sans")
rc("text", usetex=True)

class DisplayResults(object):
	def __init__(self, options):
		self.options = options

		self.data = np.loadtxt('1planet_plus_gp.rv')
		self.truth = np.loadtxt('fake_data_like_nuoph.truth')
		self.posterior_sample = np.atleast_2d(np.loadtxt('posterior_sample.txt'))

		start_parameters = 0
		# (nsamples x 1000)
		self.signals = self.posterior_sample[:, :start_parameters]

		self.extra_sigma = self.posterior_sample[:, start_parameters]
		self.eta1, self.eta2, self.eta3, self.eta4 = self.posterior_sample[:, start_parameters+1:start_parameters+5].T


		start_objects_print = start_parameters + 5
		# how many parameters per component
		self.n_dimensions = int(self.posterior_sample[0, start_objects_print])
		# maximum number of components
		self.max_components = int(self.posterior_sample[0, start_objects_print+1])

		n_dist_print = 3

		self.index_component = start_objects_print + 1 + n_dist_print + 1

		self.get_marginals()
		if '1' in options:
			self.make_plot1()
		elif '2' in options:
			self.make_plot2()
		elif '3' in options:
			self.make_plot3()
		elif '4' in options:
			self.make_plot4()
		elif '5' in options:
			self.make_plot5()


	def make_plot1(self):
		figure()
		hist(self.posterior_sample[:, self.index_component], 100)
		xlabel('Number of Planets')
		ylabel('Number of Posterior Samples')
		xlim([-0.5, 10.5])
		show()

	def get_marginals(self):
		max_components = self.max_components
		index_component = self.index_component

		# periods
		i1 = 0*max_components + index_component + 1
		i2 = 0*max_components + index_component + max_components + 1
		s = np.s_[i1 : i2]
		self.T = self.posterior_sample[:,s]
		self.Tall = np.copy(self.T)

		# amplitudes
		i1 = 1*max_components + index_component + 1
		i2 = 1*max_components + index_component + max_components + 1
		s = np.s_[i1 : i2]
		self.A = self.posterior_sample[:,s]

		# eccentricities
		i1 = 3*max_components + index_component + 1
		i2 = 3*max_components + index_component + max_components + 1
		s = np.s_[i1 : i2]
		self.E = self.posterior_sample[:,s]

		which = self.T != 0
		self.T = self.T[which].flatten()
		self.A = self.A[which].flatten()
		self.E = self.E[which].flatten()
		# Trim
		#s = sort(T)
		#left, middle, right = s[0.25*len(s)], s[0.5*len(s)], s[0.75*len(s)]
		#iqr = right - left
		#s = s[logical_and(s > middle - 5*iqr, s < middle + 5*iqr)]

	def make_plot2(self):
		figure()
		hist(np.exp(T), bins=np.logspace(min(T), max(T), base=np.e), alpha=0.5)
		xlabel(r'(Period/days)')
		gca().set_xscale("log")
		#for i in xrange(1009, 1009 + int(truth[1008])):
		#  axvline(truth[i]/log(10.), color='r')
		ylabel('Number of Posterior Samples')
		show()

	def make_plot3(self):
		figure()
		subplot(2,1,1)
		#plot(truth[1009:1009 + int(truth[1008])]/log(10.), log10(truth[1018:1018 + int(truth[1008])]), 'ro', markersize=7)
		#hold(True)
		loglog(np.exp(T), A, 'b.', markersize=5)
		ylabel(r'Amplitude (m/s)')

		subplot(2,1,2)
		#plot(truth[1009:1009 + int(truth[1008])]/log(10.), truth[1038:1038 + int(truth[1008])], 'ro', markersize=7)
		#hold(True)
		semilogx(np.exp(T), E, 'b.', markersize=5)
		xlabel(r'(Period/days)')
		ylabel('Eccentricity')
		show()


	def make_plot4(self):
		figure()
		subplot(2,2,1)
		hist(eta1, bins=100)
		subplot(2,2,2)
		hist(eta2, bins=100)
		subplot(2,2,3)
		hist(eta3, bins=100)
		subplot(2,2,4)
		hist(eta4, bins=100)
		show()



	# # data[:,0] -= data[:,0].min()
	# t = np.linspace(data[:,0].min(), data[:,0].max(), 1000)
	# c = np.random.choice(, size=10, replace=False)

	# fig = figure()
	# ax = fig.add_subplot(111)
	# ax.errorbar(data[:,0], data[:,1], fmt='b.', yerr=data[:,2])
	# data_ylimits = ax.get_ylim()
	# # plot random posterior sample signals
	# ax.plot(t, signals[c, :].T, alpha=0.4)
	# ax.set_ylim(data_ylimits)
	# # ax.errorbar(data[:,0], data[:,1], fmt='b.', yerr=data[:,2])

	def make_plot5(self):
		self.periods = np.exp(self.Tall[:,0])
		self.pmin = 72.5 #self.periods.mean() - 2*self.periods.std()
		self.pmax = 74. #self.periods.mean() + 2*self.periods.std()

		self.data = np.vstack((self.periods, self.extra_sigma, self.eta1, self.eta2, self.eta3, self.eta4)).T
		print self.data.shape
		# print (self.pmin, self.pmax)
		labels = ['P', '$\sigma_{extra}$', '$\eta_1$', '$\eta_2$', '$\eta_3$', '$\eta_4$']
		
		corner.corner(self.data, labels=labels, 
			                     plot_contours=False, plot_datapoints=True, plot_density=False,
			                     hist_kwargs={'normed':True},
			                     range=[(self.pmin, self.pmax), 1., 1., 1., 1., 1.],
			                     shared_axis=True,)


		show()








# sys.exit(0)

saveFrames = False # For making movies
# if saveFrames:
#   os.system('rm Frames/*.png')

# ion()
# for i in xrange(0, posterior_sample.shape[0]):
#   hold(False)
#   errorbar(data[:,0], data[:,1], fmt='b.', yerr=data[:,2])
#   hold(True)
#   plot(t, posterior_sample[i, 0:1000], 'r')
#   xlim([-0.05*data[:,0].max(), 1.05*data[:,0].max()])
#   ylim([-1.5*max(abs(data[:,1])), 1.5*max(abs(data[:,1]))])
#   #axhline(0., color='k')
#   xlabel('Time (days)', fontsize=16)
#   ylabel('Radial Velocity (m/s)', fontsize=16)
#   draw()
#   if saveFrames:
#     savefig('Frames/' + '%0.4d'%(i+1) + '.png', bbox_inches='tight')
#     print('Frames/' + '%0.4d'%(i+1) + '.png')


# ioff()
# show()

if __name__ == '__main__':
	print 'Arguments: ', sys.argv
	try:
		options = sys.argv[1]
	except IndexError:
		options = ''

	res = DisplayResults(options)
	globals()['res'] = res


elif __name__ == 'display':
	pass
