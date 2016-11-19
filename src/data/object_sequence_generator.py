f = open('100images.txt')

lines = f.read().strip().split("\n")
imgs_as_objs = []

i = 0
while i < len(lines):

	img = int(lines[i])
	objs = int(lines[i+2])
	img_o = []
	
	for j in xrange(objs):
		o = lines[i+3+j].split(' ')[4]
		img_o.append(o)

	imgs_as_objs.append(img_o)
	i += 3+objs

f.close()
f = file('vg.lst', 'w')

for l in imgs_as_objs:
	for x in l:
		f.write(x+" ")
	f.write('\n')
