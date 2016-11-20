import sys

f = open(sys.argv[1])

lines = f.read().strip().split("\n")
imgs_as_objs = []

i = 0
while i < len(lines):

	img = int(lines[i])
	objs = int(lines[i+1])
	img_o = []
	
	for j in xrange(objs):
		o = lines[i+2+j].split(' ')[4]
		img_o.append(o)

	imgs_as_objs.append(img_o)
	i += 2+objs

f.close()
f = file('vg.lst', 'w')

for l in imgs_as_objs:
	for x in l:
		f.write(x+" ")
	f.write('\n')
