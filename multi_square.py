import numpy as np


def pyramid(x_center, y_center, layer_height, extrusion_multi, print_speed, z_bed = 10, layer = 1):
	nozzel_dia = 1.77
	syringe_dia = 22.5
	extrusion_width = 1.5 * nozzel_dia
	retraction = 3
	retraction_speed = 400
	
	x = []
	y = []
	e = [0]
	e_true = [0]

	spacing = extrusion_width - layer_height * (1 - np.pi / 4)
	# print(spacing)
	unit_E = extrusion_multi * ((extrusion_width - layer_height) * layer_height +\
		np.pi * (layer_height / 2) ** 2) / (np.pi * (syringe_dia / 2) ** 2)
	travel_speed = 6000

	# ?
	z_lift = 1

	# for future cooking setting
	cook_y_offset = -62
	# to make different layers
	# for i in range(25):
	# filename = filename + str(i) + '.gcode'


	# main loop
	# extra_extru
	file.write('G01 E2.0 F%4.2f\n'%(retraction_speed))
	file.write('G92 E0\n')

	z = z_bed + layer_height * layer

	t = list(range(5))
	t = [i * np.pi/2 for i in t]
	# print(t)

	# walls = 6
	walls = int(12.5 // spacing)
	# print(walls)
	# print(spacing * 5)

	for j in range(walls):
		x.extend([x_center + (12.5* 2**0.5 - 2**0.5*j*spacing)*np.cos(i) for i in t])
		y.extend([y_center + (12.5* 2**0.5 - 2**0.5*j*spacing)*np.sin(i) for i in t])

	for k in range(walls):
		for l in range(len(t) - 1):
			e.append(unit_E * ((x[k * len(t) + l + 1] - x[k * len(t) + l]) ** 2 +\
				(y[k * len(t) + l + 1] - y[k * len(t) + l]) ** 2) ** 0.5)


	for k in range(len(e) - 1):
		e[k + 1] = e[k + 1] + e[k]

	for k in range(walls - 1):
		e_true.extend(e[k * (len(t) - 1) + 1 : (k+1) * (len(t) - 1) + 1])
		e_true.append(e[(k + 1) * (len(t) - 1)])

	e_true.extend(e[(walls - 1) * (len(t) - 1) + 1:])


	file.write('G01 X%4.2f Y%4.2f Z%4.2f E%4.2f F%4.2f\n'%(x[0], y[0], z, e_true[0], travel_speed))
	for i in range(1, len(x)):
		file.write('G01 X%4.2f Y%4.2f Z%4.2f E%4.2f F%4.2f\n'%(x[i], y[i], z, e_true[i], print_speed))

	e_end = e[-1] - retraction
	z = z + z_lift
	file.write('G01 E%4.2f F%4.2f\n'%(e_end, retraction_speed))
	file.write('G92 E0\n')



	#x_end = x[-1] - 20
	#y[end] = y[-1] - 20
def multi_square(var, layer_height, extrusion_multi, print_speed, step):
	x_center = [60, 100, 140, 60, 100, 140]
	y_center = [100, 100, 100, 140, 140, 140]
	if var == 'layer_height':
		for i in range(len(x_center)):
			pyramid(x_center[i], y_center[i], layer_height + i * step, extrusion_multi, print_speed)	
	elif var == 'extrusion_multi':
		for i in range(len(x_center)):
			pyramid(x_center[i], y_center[i], layer_height, extrusion_multi + i * step, print_speed)
	else:
		for i in range(len(x_center)):
			pyramid(x_center[i], y_center[i], layer_height, extrusion_multi, print_speed + i * step)
		



	
filename = 'multi_test'
filename = filename + '.gcode'
file = open(filename, 'w')

file.write('G21\n')
file.write('G90\n')
file.write('M82\n')
file.write('G01 F6000\n')
file.write('T0\n')
file.write('G92 E0\n')
file.write('G28 X Y Z\n')
multi_square('layer_height', 1.0, 1.0, 1200, 0.1)

file.close()




