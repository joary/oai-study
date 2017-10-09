
import subprocess

base_url = 'https://github.com/joary/openairinterface5g'
def regen_line(line, info):

	if(len(info) == 0):
		return line


	new_l = line;
	for i in info:
		src = i[0]
		srcl = str(i[1])
		func = i[2]

		link = base_url+'/'+src+'#'+srcl
		info_rep = '['+func+'()]('+link+')'
		new_l = new_l.replace(func+'()', info_rep)
	return new_l

def cscope_search_func(fname):
	result = subprocess.run(['bash', 'run_cscope.sh', fname], stdout=subprocess.PIPE)
	res = result.stdout.decode('utf-8');

	func_info = ''
	lines = res.split('\n')
	for l in lines:
		n = l.count(fname)
		if n == 2:
			func_info = l;
			break;

	src = ''
	src_line = 0
	if(func_info != ''):
		func_info = func_info.split(' ')
		src = func_info[0]
		src_line = int(func_info[2])
		
	return (src, src_line, fname)

def get_function_name(f_str):
	tmp = f_str.split('()')
	tmp = tmp[0]
	tmp = tmp.strip('*')
	tmp = tmp.strip('`')
	return tmp;

def parse_tmpl(fname, outf):
	f = open(fname)
	a = f.readlines();
	f.close()

	ret = []

	for l in a:
		info = []
		for field in l.split(' '):
			if '()' in field:
				func = get_function_name(field)
				data = cscope_search_func(func)
				if(data[0] != ''):
					info += [data]
		new_l = regen_line(l, info)
		ret += [new_l]

	f2 = open(outf, 'w')
	f2.writelines(ret)
	f2.close()

	return ret
