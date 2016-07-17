#coding=utf-8
import requests
from PIL import Image
import StringIO
import time
import re
import nku_sss_ocr
if __name__ == '__main__':

	V = nku_sss_ocr.Val_to_Str()
	postdata = {
			"operation":"",
			"usercode_text":"4878481",
			"userpwd_text":"12214144",
			"checkcode_text":"",
			"submittype":"\xC8\xB7 \xC8\xCF"
		}
	F = 0
	SU = 3000
	i = 0
	T = []
	while i < SU:
		try:
			i += 1
			G = requests.session()
			S = Image.open(StringIO.StringIO(G.get("http://222.30.32.10/ValidateCode", timeout = 6).content))
			STA = time.time()
			postdata["checkcode_text"] = V.IM_to_Str_MatDiff2(S)
			D_Time = time.time()-STA
			print D_Time, "\t%s/%s"%(i,SU), 
			if re.findall(u"正确的验证码".encode("GBK"), G.post("http://222.30.32.10/stdloginAction.do", data = postdata, timeout = 6).content):
				F += 1
				print False
			else:
				print True
			T.append(D_Time)
		except KeyboardInterrupt:
			break
		except:
			print "Error Occured"
			# raise
	print u"错误%s/总计%s/每次识别耗时%.04fs"%(F, i, sum(T)/len(T))