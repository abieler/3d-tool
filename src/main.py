from __future__ import division
import datetime
import spice
from abieler.shapeUtils import *
import mayavi.mlab as mlab
import numpy as np

#spice.furnsh("/home/abieler/rosetta/spiceKernels/metafiles/operationalKernels.tm")
spice.furnsh("/home/abieler/rosetta/spiceKernels/metafiles/operationalKernelsSHAP5.tm")
#spice.furnsh("/home/abieler/rosetta/spiceKernels/metafiles/operationalKernels.tm")
t = datetime.datetime(2014,8,23,11,58)
timeStamp = datetime.datetime.strftime(t, '%Y-%m-%dT%H:%M:%S')
et = spice.str2et(timeStamp)
R = spice.pxform('ROS_VIRTIS_M','67P/C-G_CK', et)

rSC, lt = spice.spkpos('ROSETTA', et, '67P/C-G_CK', 'NONE', 'CHURYUMOV-GERASIMENKO')
rSC = np.array(rSC, dtype=float)
rSC_hat = rSC / np.linalg.norm(rSC)

rSun, lt = spice.spkpos("SUN", et, "67P/C-G_CK", "NONE", "CHURYUMOV-GERASIMENKO")
rSun = np.array(rSun, dtype=float)
rSun_hat = rSun / np.linalg.norm(rSun)

fStretch = 4000

xSC_plt = np.array([0.0, rSC_hat[0]]) * fStretch
ySC_plt = np.array([0.0, rSC_hat[1]]) * fStretch
zSC_plt = np.array([0.0, rSC_hat[2]]) * fStretch
#rSun, lt = spice.spkpos("SUN", et, "J2000", "NONE", "CHURYUMOV-GERASIMENKO")

xSun_plt = np.array([0.0, rSun_hat[0]]) * fStretch
ySun_plt = np.array([0.0, rSun_hat[1]]) * fStretch
zSun_plt = np.array([0.0, rSun_hat[2]]) * fStretch

fileName = '/home/abieler/rosetta/shapeModel/meshes/OSIRIS/SHAP5_vStefano/SHAP5_stefano.ply'
nTriangles, nodeCoords, triIndices, triangles, n_hat, triCenters, triAreas = load_shape_model_vtk(fileName)

x = nodeCoords[:,0]
y = nodeCoords[:,1]
z = nodeCoords[:,2]

phaseAngle = np.zeros(nTriangles)
for i in range(nTriangles):
  phaseAngle[i] = angle_between(rSun_hat, n_hat[i])


s = mlab.pipeline.triangular_mesh_source(x, y, z, triIndices)
s.data.cell_data.scalars = np.cos(phaseAngle)
surf = mlab.pipeline.surface(s)
surf.contour.filled_contours = True
surf.contour.minimum_contour = 0.0
surf.contour.maximum_contour = 1.0
surf.module_manager.scalar_lut_manager.data_range = (0,1)
mlab.plot3d(xSun_plt, ySun_plt, zSun_plt, tube_radius=20, color=(1,1,0))
mlab.plot3d(xSC_plt, ySC_plt, zSC_plt, tube_radius=20, color=(0,0,1))
mlab.view()
#mlab.view(distance=dist/5, elevation=180, roll=-90, focalpoint=(0,0,dist))

print mlab.view()
mlab.show()
