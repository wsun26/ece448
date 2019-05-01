def plotWeights(weights,num):
	num_mat = [[0.0 for x in range(28)] for y in range(28)]
	
	for i in range(784):
		num_mat[i/28][i%28] = weights[num][i]

	plt.subplot(111)
	plt.imshow(num_mat,cmap='plasma',interpolation='nearest')
	plt.title('Weights for Number '+str(num))
	plt.colorbar()

	plt.show()