#coding=utf-8
import FindChr
import numpy
import DiffMat
import os, zlib, base64, difflib, json, re

class Val_to_Str():
	"""
	Usage:
		from PIL import Image
		OCRobj = Val_to_Str()
		Im = Image.open("Test.jpg")
		print OCRobj.IM_to_Str_MatDiff(Im)
	"""
	def __init__(self):
		self.DB = json.loads(open(os.path.split(os.path.realpath(__file__))[0]+"/lib.txt").read())
		for i in self.DB.keys():
			self.DB[i] = self.base64_zlib_json_load(self.DB[i])
		self.DB = reduce(lambda x, y:x.extend(y) or x, map(lambda x:map(lambda x, y:[x, y], [x[0], ]*len(x[1]), x[1]), self.DB.items()))
		self.DB_Matrix = map(lambda x: [x[0], numpy.array(map(lambda x: map(lambda x: int(x),list(x)), re.split('\/', x[1])))], self.DB)


	def base64_zlib_json_load(self, String):
		return json.loads(zlib.decompress(base64.b64decode(String)))


	def IM_to_Str_MatDiff(self, im):
		CHRS = FindChr.CutBox(im)
		RES = ""
		for i in CHRS:
			D = numpy.where(numpy.array(i) == 255, 1, 0)
			G = map(lambda x,y: [y, DiffMat.Diff_Matrix(x, y[1])], [D ,]*len(self.DB_Matrix), self.DB_Matrix)
			Q = sorted(G, key = lambda x:(x[1][0]+x[1][1]))[-1]
			RES += Q[0][0]
		return RES


