from multiprocessing import Pool
def f(x):
	return x*x

if __name__=='_main_':
	p=Pool(5)
        res= p.map(f,[1,2,3])
	print(p.map(f,[1,2,3]))
        cleaned = [x for x in result if not x is None ]
        cleaned = asarry(clearned)
        p.close()
	p.join()
