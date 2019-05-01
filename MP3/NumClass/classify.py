#!/usr/bin/python
from numio import *
from math import log
import sys
import matplotlib.pyplot as plt
import numpy as np

def trainData(i_file_name,l_file_name,length):

	k = 0.0000001					#smoothing constant
	V = 2							#number of features
	cond_p = [[0 for x in range(784)] for y in range(10)]
	p_class = [0 for x in range(10)]
	for i in range(length):
		n, f = readNumber(i_file_name,l_file_name,i)
		for j in range(784):
			if(f[j]!=' '):
				cond_p[n][j]+=1
		p_class[n]+=1

	for i in range(10):
		for j in range(784):
			cond_p[i][j] = (float(cond_p[i][j]+k))/(p_class[i]+k*V)
		p_class[i]/=float(length)
	
	return (cond_p,p_class)

def classifyImages(i_file_name,l_file_name,length,cond_p,p_class):
	classified_list = [(0,0) for x in range(length)]
	best_match_val = [-sys.maxint - 1 for x in range(10)]
	best_match = [['0' for x in range(784)] for y in range(10)]
	worst_match_val = [1 for x in range(10)]
	worst_match = [['0' for x in range(784)] for y in range(10)]
	for i in range(length):
		n, f = readNumber(i_file_name,l_file_name,i)
		max_prob = -sys.maxint - 1
		likely_num = -1
		for j in range(10):
			cur_prob = log(p_class[j])
			for k in range(784):
				if(f[k]!=' '):
					cur_prob += log(cond_p[j][k])
				else:
					cur_prob += log(1-cond_p[j][k])
			if(cur_prob>max_prob):
				max_prob = cur_prob
				likely_num = j
			if(cur_prob>best_match_val[j]):
				best_match_val[j] = cur_prob
				best_match[j] = f[:]
			if(cur_prob<worst_match_val[j]):
				worst_match_val[j] = cur_prob
				worst_match[j] = f[:]
		classified_list[i] = (likely_num,n)
	return (classified_list, best_match, worst_match)

def plotOddRatios(cond_p,num1,num2):
	num1_mat = [[0.0 for x in range(28)] for y in range(28)]
	min_val = 0.005
	for i in range(784):
		if(cond_p[num1][i]>min_val):
			num1_mat[i/28][i%28] = log(cond_p[num1][i])
		else:
			num1_mat[i/28][i%28] = log(min_val)

	num2_mat = [[0.0 for x in range(28)] for y in range(28)]
	for i in range(784):
		if(cond_p[num2][i]>min_val):
			num2_mat[i/28][i%28] = log(cond_p[num2][i])
		else:
			num2_mat[i/28][i%28] = log(min_val)

	odd_mat = [[0.0 for x in range(28)] for y in range(28)]
	for i in range(784):
		p1 = cond_p[num1][i]
		if(p1<=min_val):
			p1 = min_val
		p2 = cond_p[num2][i]
		if(p2<=min_val):
			p2 = min_val
		odd_mat[i/28][i%28] = log(p1/p2)

	plt.subplot(334)
	plt.imshow(num1_mat,cmap='plasma',interpolation='nearest')
	plt.title('Number '+str(num1))
	plt.colorbar()

	plt.subplot(335)
	plt.imshow(num2_mat,cmap='plasma',interpolation='nearest')
	plt.title('Number '+str(num2))
	plt.colorbar()

	plt.subplot(336)
	plt.imshow(odd_mat,cmap='plasma',interpolation='nearest')
	plt.title('Odd Ratio Between '+str(num1)+' and '+str(num2))
	plt.colorbar()

	plt.show()


cond_p, p_class = trainData("trainingimages","traininglabels",5000)

num_tests = 1000
class_l, best_match, worst_match = classifyImages("testimages","testlabels",num_tests,cond_p,p_class)

conf_mtx = [0 for x in range(100)]
num_correct = 0.0
ind_num_correct = [0.0 for x in range(10)]
ind_sum = [0 for x in range(10)]

plotOddRatios(cond_p,9,4)
plotOddRatios(cond_p,9,7)
plotOddRatios(cond_p,3,8)
plotOddRatios(cond_p,3,5)

for i in range(num_tests):
	conf_mtx[class_l[i][0]*10+class_l[i][1]] += 1
	if(class_l[i][0] == class_l[i][1]):
		num_correct+=1.0
		ind_num_correct[class_l[i][0]]+=1.0
	ind_sum[class_l[i][1]]+=1.0

out_str = 'Number Classification Report: \n\n'
out_str += 'Number of Training Images: '+str(5000)+'\n'
out_str += 'Training Image File: trainingimages\n'
out_str += 'Training Label File: traininglabels\n\n'

out_str += 'Number of Test Images: '+str(1000)+'\n'
out_str += 'Test Image File: testimages\n'
out_str += 'Test Label File: testlabels\n\n'

out_str += 'Confusion Matrix: \n'

out_str += '|\t |0\t|1\t|2\t|3\t|4\t|5\t|6\t|7\t|8\t|9\t|\n'
out_str += '-----------------------------------------------------------------------------------------\n'
for i in range(10):
	cur_str = ''
	for j in range(10):
		cur_str+='|'+str(conf_mtx[i*10+j])+'\t'
	out_str+= '|\t'+str(i)+cur_str+'|\n'
out_str += '-----------------------------------------------------------------------------------------\n'


out_str += "% Correct Overall: "+str(num_correct/num_tests*100)+'\n'

print "% Correct Overall: "+str(num_correct/num_tests*100)

out_str += '\n'
for i in range(10):
	out_str += '####################___'+str(i)+'___####################\n'
	out_str += "% Correct for "+str(i)+": "+str(ind_num_correct[i]/ind_sum[i]*100)+'\n'
	out_str += '\nBest Match for '+str(i)
	for j in range(28):
		cur_str = ''
		for k in range(28):
			cur_str += best_match[i][j*28+k] 
		out_str += cur_str+'\n'
	out_str += '\nWorst Match for '+str(i)
	for j in range(28):
		cur_str = ''
		for k in range(28):
			cur_str += worst_match[i][j*28+k] 
		out_str += cur_str+'\n'

#print out_str

out_file = open('classify_report.txt','w')
out_file.write(out_str)
out_file.close()