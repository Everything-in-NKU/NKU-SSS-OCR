import nku_sss_ocr
import DiffMat
import json, zlib, base64
import numpy
C = nku_sss_ocr.Val_to_Str()
M = C.DB_Matrix
chrs = set([i[0] for i in M])
D = {}
E = {}
for i in chrs:
    D[i] = []
for i in M:
    D[i[0]].append(i[1])

def merge(Mat1, Mat2):
    A, B = Mat1, Mat2
    sim, D1, Max = DiffMat.Diff_Matrix_Merge(A, B)
    N_array = numpy.zeros(Max, dtype = numpy.int32)
    M1, M2, M = D1
    N1, N2 = A.shape, B.shape
    N_array[M2[0]:(M2[0]+N1[0]), M2[1]:(M2[1]+N1[1])] += A
    N_array[M1[0]:(M1[0]+N2[0]), M1[1]:(M1[1]+N2[1])] += B
    return N_array

for i in chrs:
    T = reduce(merge, D[i]).astype(numpy.int32)
    
    M, N = (T>7).any(0).tolist(), (T>7).any(1).tolist()
    X = (len(M) - M[::-1].index(True) + 1) - (M.index(True) + 1)
    Y = (len(N) - N[::-1].index(True) + 1) - (N.index(True) + 1)
    T = [base64.b64encode(zlib.compress(json.dumps(T.tolist()), 9)), (Y, X)]
    E[i] = T
    



with open("lib2_alpha_and_num.txt", "w") as f:
    f.write(json.dumps(E))



