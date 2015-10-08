import numpy as np

def calculate_triangle_area(triangles):

    triArea = []
    for triangle in triangles:
        P = triangle[1] - triangle[0]
        Q = triangle[2] - triangle[0]
        S = np.sqrt(np.sum(np.cross(P, Q)**2))
        triArea.append(S)
    return 0.5 * abs(np.array(triArea))


def calculate_surface_normals(vertexes, triangles):

    nTriangles = triangles.shape[0]
    print '%i triangles' % nTriangles

    n_hat = np.zeros((nTriangles, 3))
    for ii, indexSet in enumerate(triangles):
        i,j,k = indexSet
        n_hat[ii] = np.cross((vertexes[j] - vertexes[i]), (vertexes[k] - vertexes[i]))
        n_hat[ii] = n_hat[ii] / np.sqrt(((n_hat[ii]**2).sum()))

    return n_hat
def load_shape_model_vtk(fileName, fileType='vtk'):
    
    if fileName.split('.')[-1] =='ply':
      fileType = 'ply'

    # process file header
    with open(fileName, 'r') as iFile:
      if fileType == 'vtk':
	    for i, line in enumerate(iFile):
		if 'POINTS' in line:
		    iPoints = i + 1
		elif 'CELLS' in line:
		    iCells = i + 1
		elif 'CELL_TYPES' in line:
		    iCellTypes = i + 1
	    iMax = i
      elif fileType == 'ply':
	for i, line in enumerate(iFile):
	  if 'element vertex' in line:
	    iPoints = int(line.split(' ')[2])
	  elif 'element face ' in line:
	    iCells = int(line.split(' ')[2])
	  elif 'end_header' in line:
	    iHeader = i+1
	    break
    if fileType == 'vtk':
      x,y,z = np.genfromtxt(fileName, delimiter=' ', skip_header=iPoints,
			      unpack=True, skip_footer=(iMax-iCells+1))
      triIndices = np.genfromtxt(fileName, delimiter=' ', skip_header=iCells,
				skip_footer=(iMax-iCellTypes+1))
    elif fileType == 'ply':
      x, y, z = np.genfromtxt(fileName, delimiter=' ', dtype=float, skiprows=iHeader,
			      unpack=True, skip_footer=(iCells), usecols=(0,1,2))
      triIndices = np.genfromtxt(fileName, delimiter=' ', skip_header=(iHeader+iPoints),
				 usecols=(0,1,2,3), dtype=int)

    nodeCoords = np.array([[xx, yy, zz] for xx,yy,zz in zip(x,y,z)])

    nTriangles = triIndices.shape[0]

    triIndices = np.array([[i,j,k] for i,j,k in zip(triIndices[:,1], triIndices[:,2], triIndices[:,3])], dtype=int)
    triangles = np.array([[nodeCoords[iSet[0]], nodeCoords[iSet[1]], nodeCoords[iSet[2]]] for iSet in triIndices], dtype=float)

    n_hat = calculate_surface_normals(nodeCoords, triIndices)
    n_hat = np.array(n_hat, dtype=float)

    p = np.array([[triangles[i,:,0].sum()/3, triangles[i,:,1].sum()/3,triangles[i,:,2].sum()/3] for i in range(nTriangles)])

    # calculate surface area of each triangle
    triArea = calculate_triangle_area(triangles)

    return nTriangles, nodeCoords, n_hat, triIndices


def plt_coords(a,b, fStretch=1):

    coords = np.zeros((2,3))
    coords[0,:] = a
    coords[1,:] = a+b

    xPlt = coords[:,0] * fStretch
    yPlt = coords[:,1] * fStretch
    zPlt = coords[:,2] * fStretch

    return xPlt, yPlt, zPlt


def angle_between(v1, v2):

    angle = np.arccos(np.dot(v1, v2))
    if np.isnan(angle):
        if (v1 == v2).all():
            return 0.0
        else:
            return np.pi
    return angle
