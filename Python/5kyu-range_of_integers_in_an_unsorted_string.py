import math
import re
def mystery_range(s,n):
	if n == 100:
		min_digit = math.floor(len(s)/n - 0.1)
	else:
		min_digit = math.floor(len(s)/n)
	char_list = list(s)
	a=0
	f = True
	while f:
		if a>= len(s):
			numbers = []
			break
		if min_digit != 0:
			min_candidate = int(s[a:a+min_digit])
		mn = min_candidate
		for i in range(n-1):
			mn +=1
			pattern = str(mn) + '+'
			if re.search(pattern,s) is None:
				f = True
				break
			else:
				f = False
		if not f:
			res = ''.join(str(c) for c in range(min_candidate,mn+1))
			if sorted(res) == sorted(char_list):
				numbers = [min_candidate,mn]
			else:
				f = True
		a +=1
	return numbers

mystery_range('6510471823593224504031702384587543101685646852229769112692556056767872151793774238441810625103961941627989100391085351365710263914730889812952933802145862046546761591053734997349278387811448281394741016610790',100)
