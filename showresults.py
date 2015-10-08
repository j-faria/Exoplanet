import sys
try:
	options = sys.argv[1]
except IndexError:
	options = ''


import postprocess
logz_estimate, H_estimate, logx_samples, posterior_sample = postprocess.postprocess(cut=0.)
if posterior_sample.shape[0] > 5:
	import display
	res = display.DisplayResults(options)
else:
	print 'Too few samples yet'

