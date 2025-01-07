
point_coordinate = {'K':[0.33333333333,0.3333333333,0],'M':[0,0.5,0],'G':[0,0,0]}

def band_points (points):
    point_list =[]
    for point in points:
        coordinate = symmetry_coordinate(point)
        point_list.append(coordinate)
    return point_list

def symmetry_coordinate(point):
    point = point.upper()
    coordinate = point_coordinate[point]
    return coordinate

# def band_input(points,num_points):
#     coordinates = band_points(points)
#     parameter = []
#     for j,i in enumerate(coordinates):
#         input_line = {'x':str(i[0]),'y':str(i[1]),'z':str(i[2]),'number':str(num_points),'label':f" ! {points[j].upper()}"}
#         parameter.append(input_line)
#     return parameter


def band_input(label,points,num_points):
    parameter = []
    for k,j in enumerate(points):
        if k == len(label)-1:
            input_line = {'x':str(j[0]),'y':str(j[1]),'z':str(j[2]),'number':str(1),'label':f"{label[k].upper()}"}
        else:
            input_line = {'x':str(j[0]),'y':str(j[1]),'z':str(j[2]),'number':str(num_points),'label':f"{label[k].upper()}"}
        parameter.append(input_line)
    return parameter
