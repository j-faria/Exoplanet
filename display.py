from pylab import *
import os
import sys

rc("font", size=14, family="serif", serif="Computer Sans")
rc("text", usetex=True)

data = loadtxt('fake_data_like_nuoph.txt')
truth = loadtxt('fake_data_like_nuoph.truth')
posterior_sample = atleast_2d(loadtxt('posterior_sample.txt'))

start_objects_print = 5
# how many parameters per component
n_dimensions = int(posterior_sample[0, start_objects_print])
# maximum number of components
max_components = int(posterior_sample[0, start_objects_print+1])

n_dist_print = 3

index_component = start_objects_print + 1 + n_dist_print + 1

hist(posterior_sample[:,index_component], 100)
xlabel('Number of Planets')
ylabel('Number of Posterior Samples')
xlim([-0.5, 10.5])
# show()

# periods
i1 = 0*max_components + index_component + 1
i2 = 0*max_components + index_component + max_components + 1
s = np.s_[i1 : i2]
T = posterior_sample[:,s]

# amplitudes
i1 = 1*max_components + index_component + 1
i2 = 1*max_components + index_component + max_components + 1
s = np.s_[i1 : i2]
A = posterior_sample[:,s]

# eccentricities
i1 = 3*max_components + index_component + 1
i2 = 3*max_components + index_component + max_components + 1
s = np.s_[i1 : i2]
E = posterior_sample[:,s]

which = T != 0
T = T[which].flatten()
A = A[which].flatten()
E = E[which].flatten()
# Trim
#s = sort(T)
#left, middle, right = s[0.25*len(s)], s[0.5*len(s)], s[0.75*len(s)]
#iqr = right - left
#s = s[logical_and(s > middle - 5*iqr, s < middle + 5*iqr)]

figure()
hist(np.exp(T), bins=np.logspace(min(T), max(T), base=np.e), alpha=0.5)
xlabel(r'(Period/days)')
gca().set_xscale("log")
#for i in xrange(1009, 1009 + int(truth[1008])):
#  axvline(truth[i]/log(10.), color='r')
ylabel('Number of Posterior Samples')
# show()

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

sys.exit(0)

# data[:,0] -= data[:,0].min()
# t = linspace(data[:,0].min(), data[:,0].max(), 1000)

# saveFrames = False # For making movies
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
