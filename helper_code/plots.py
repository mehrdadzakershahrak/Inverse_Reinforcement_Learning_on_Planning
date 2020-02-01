import numpy as np
import matplotlib.pyplot as plt
grads = np.load('theta_plot.npy')
thetas = np.load('final_thetas.npy')
#for i in range(np.shape(grads)[1]):
#labels = ['lav','plan','cost','x','y']
labels = ['lav','cost_sq','a1','a2','a3','a4']
thetas = np.load('final_thetas.npy')
print(thetas)
#print(grads)

for i in range(np.shape(grads)[1]):
	#if i <=2:
		plt.plot(grads[:,i],label = labels[i])
	#else:
		#plt.plot(grads[:, i])
	#	print("See")
plt.legend(loc='best')
plt.show()