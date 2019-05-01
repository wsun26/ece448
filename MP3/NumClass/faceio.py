#!/usr/bin/python

def readFace(i_file_name, l_file_name, i):
	i_file = open(i_file_name,'r')
	l_file = open(l_file_name,'r')

	num = -1
	f = [0 for x in range(60*70)]

	i_file.seek(i*61*70,0)
	l_file.seek(i*2,0)

	num = (int)(l_file.read(1))

	for j in range(70):
		cur_str = i_file.readline()
		for k in range(60):
			f[j*60+k] = cur_str[k]

	i_file.close()
	l_file.close()

	return (num,f)