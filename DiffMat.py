import numpy

# def DiffSqrt(Mat1, Mat2):
# 	if Mat1.shape != Mat2.shape:
# 		return 0.0
# 	F = numpy.where(Mat1 == Mat2, 1, 0).reshape((1,-1))[0]
# 	C = list(numpy.bincount(F))
# 	J = F.shape[0]
# 	if len(C) <= 1:
# 		D = 0
# 	else:
# 		D = C[1]
# 	return float(D)/J, J

def DiffSqrt(Mat1, Mat2):  #An equivalent of the previous version
	assert Mat1.shape == Mat2.shape
	D = numpy.count_nonzero(Mat1 == Mat2)
	J = Mat1.size
	return float(D)/J, J

def DiffSqrt2(Mat1, Mat2):  # Equivalent of DiffSqrt_Merge with some magic number 
	assert Mat1.shape == Mat2.shape
	#Mat1 will be the Sample
	if Mat1.max() > 5:
		Mat1, Mat2 = Mat2, Mat1
	D = numpy.sum(Mat2*Mat1)/10
	E = numpy.count_nonzero((~(Mat2>>3)+2) & (~Mat1+2)) 
	J = Mat1.size
	return float(D+E)/J, J

def DiffSqrt_Merge(Mat1, Mat2):
	assert Mat1.shape == Mat2.shape
	D = numpy.sum(Mat2*Mat1)/(Mat1.max()*Mat2.max())
	E = numpy.count_nonzero((Mat1<(0.75*Mat1.max())) & (Mat2<(0.75*Mat2.max())) )
	J = Mat1.size
	return float(D+E)/J, J

def FitSizes(Mat1, Mat2):
	#print Mat2, Mat1
	if len(Mat2.shape) != 2 or len(Mat1.shape) != 2:
		pass
	else:
		S1, S2 = Mat1.shape, Mat2.shape
		Max = [max(S1[0], S2[0]), max(S1[1], S2[1])]
		Min = [min(S1[0], S2[0]), min(S1[1], S2[1])]
		for i, j in [(i1, j1) for i1 in range(S1[0] - Min[0]+1) for j1 in range(S1[1]-Min[1]+1)]:
			for k, l in [(i2, j2) for i2 in range(S2[0] - Min[0]+1) for j2 in range(S2[1]-Min[1]+1)]:
				#print  ((Mat1[i:(i+Min[0]) ,j:(j+Min[1]) ], Mat2[ k:(k+Min[0]) ,l:(l+Min[1]) ]), [[i ,j ], [k, l], float(Min[0]*Min[1])/float(Max[0]*Max[1])])
				yield ((Mat1[i:(i+Min[0]) ,j:(j+Min[1]) ], Mat2[ k:(k+Min[0]) ,l:(l+Min[1]) ]), [[i ,j ], [k, l], float(Min[0]*Min[1])/float(Max[0]*Max[1])])
				
def Diff_Matrix(Mat1, Mat2):
	H = max([(DiffSqrt(*i[0]), i[1])  for i in FitSizes(Mat1, Mat2)], key = lambda x:x[0][0])
	H = [H[0][0], H[1][2]]
	return H

def Diff_Matrix2(Mat1, Mat2):
	H = max([(DiffSqrt2(*i[0]), i[1])  for i in FitSizes(Mat1, Mat2)], key = lambda x:x[0][0])
	H = [H[0][0], H[1][2]]
	return H

def Diff_Matrix_Merge(Mat1, Mat2):
	H = max([(DiffSqrt_Merge(*i[0]), i[1])  for i in FitSizes(Mat1, Mat2)], key = lambda x:x[0][0])
	H = [H[0][0], H[1][2]]
	return H


if __name__ == '__main__':
	Q = numpy.array([[1,0,1],[1,1,0],[1,1,1]])
	P = numpy.array([[1,0,0],[1,0,0],[1,0,1]])
	print "Different between\n", P, "\n",Q, "\nis", DiffSqrt(P, Q)

	R = numpy.array(
			[
				[1,0,1],
				[1,1,1],
				[1,1,0],
				[0,1,0],
			]
		)
	S = numpy.array(
			[
				[1,0,1,0],
				[0,1,1,1],
				[1,1,0,1],
			]
		)
	for M in FitSizes(R,S):
		print M
		print DiffSqrt(*M[0])

	print Diff_Matrix(R,S)


