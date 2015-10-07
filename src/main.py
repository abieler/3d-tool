from __future__ import division
import datetime
import spice
from helpers import *
import mayavi.mlab as mlab
import numpy as np


r_hat_virtis = np.array([0,0,1])
spice.furnsh("../input/spiceMetafile.tm")
t = datetime.datetime(2014,8,23,11,58)
timeStamp = datetime.datetime.strftime(t, '%Y-%m-%dT%H:%M:%S')
et = spice.str2et(timeStamp)
R = spice.pxform('ROS_OSIRIS_NAC','67P/C-G_CK', et)
r_hat_virtis = np.dot(R, r_hat_virtis)

rSC, lt = spice.spkpos('ROSETTA', et, '67P/C-G_CK', 'NONE', 'CHURYUMOV-GERASIMENKO')
rSC = np.array(rSC, dtype=float)
rSC_hat = rSC / np.linalg.norm(rSC)

rSun, lt = spice.spkpos("SUN", et, "67P/C-G_CK", "NONE", "CHURYUMOV-GERASIMENKO")
rSun = np.array(rSun, dtype=float)
rSun_hat = rSun / np.linalg.norm(rSun)

fStretch = 1

xSC_plt = np.array([0.0, rSC_hat[0]]) * fStretch
ySC_plt = np.array([0.0, rSC_hat[1]]) * fStretch
zSC_plt = np.array([0.0, rSC_hat[2]]) * fStretch

xSun_plt = np.array([0.0, rSun_hat[0]]) * fStretch
ySun_plt = np.array([0.0, rSun_hat[1]]) * fStretch
zSun_plt = np.array([0.0, rSun_hat[2]]) * fStretch

xVIRTIS_plt = np.array([rSC_hat[0], rSC_hat[0]+r_hat_virtis[0]])
yVIRTIS_plt = np.array([rSC_hat[1], rSC_hat[1]+r_hat_virtis[1]])
zVIRTIS_plt = np.array([rSC_hat[2], rSC_hat[2]+r_hat_virtis[2]])

fileName = '../input/shapeModel.ply'
nTriangles, nodeCoords, triIndices, triangles, n_hat, triCenters, triAreas = load_shape_model_vtk(fileName)

x = nodeCoords[:,0] - np.mean(nodeCoords[:,0])
y = nodeCoords[:,1] - np.mean(nodeCoords[:,1])
z = nodeCoords[:,2] - np.mean(nodeCoords[:,2])

phaseAngle = np.zeros(nTriangles)
for i in range(nTriangles):
  phaseAngle[i] = angle_between(rSun_hat, n_hat[i])


print xVIRTIS_plt
print yVIRTIS_plt
print zVIRTIS_plt

s = mlab.pipeline.triangular_mesh_source(x, y, z, triIndices)
s.data.cell_data.scalars = np.cos(phaseAngle)
surf = mlab.pipeline.surface(s)
surf.contour.filled_contours = True
surf.contour.minimum_contour = 0.0
surf.contour.maximum_contour = 1.0
surf.module_manager.scalar_lut_manager.data_range = (0,1)
mlab.plot3d(xSun_plt, ySun_plt, zSun_plt, tube_radius=0.003, color=(1,1,0))
mlab.plot3d(xSC_plt, ySC_plt, zSC_plt, tube_radius=0.003, color=(0,0,1))
mlab.plot3d(xVIRTIS_plt, yVIRTIS_plt, zVIRTIS_plt, tube_radius=0.003, color=(0,0,0))
mlab.view()
#mlab.view(distance=dist/5, elevation=180, roll=-90, focalpoint=(0,0,dist))

print mlab.view()
mlab.show()
