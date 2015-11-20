from __future__ import division
import datetime
from helpers import *
from virtis import pointing_vectors
import numpy as np

import mayavi.mlab as mlab
from mayavi import mlab
mlab.options.backend = 'envisage'

# load spice kernels
try:
    import spiceypy as spice
except:
    import spice

def picker_callback(picker):
    v = mlab.view()
    return v

def hide_elements(vtk_obj, event):
    v = mlab.view()
    v = mlab.view()
    mlab.clf()
    draw_nucleus(v)

def draw_scene():
    s = mlab.pipeline.triangular_mesh_source(x, y, z, triIndices)
    s.data.cell_data.scalars = np.cos(phaseAngle)
    surf = mlab.pipeline.surface(s)
    surf.contour.filled_contours = True
    surf.contour.minimum_contour = 0.0
    surf.contour.maximum_contour = 1.0
    surf.module_manager.scalar_lut_manager.data_range = (0,1)
    mlab.plot3d(xSun_plt, ySun_plt, zSun_plt, tube_radius=fStretch/1000, color=(1,1,0))
    mlab.plot3d(xSC_plt, ySC_plt, zSC_plt, tube_radius=fStretch/1000, color=(0,0,1))

    ball_x = []
    ball_y = []
    ball_z = []
    for i in range(nPixelsX):
        for j in range(nPixelsY):
            p = np.dot(R, pVectors[:,i,j])
            p_tan = np.dot(rCG, p) * p + rSC

            xVIR_plt, yVIR_plt, zVIR_plt = plt_coords(rSC,  1.1*fStretch*p)
            mlab.plot3d(xVIR_plt, yVIR_plt, zVIR_plt, tube_radius=fStretch/5000, color=(0,0,0))
            ball_x.append(p_tan[0])
            ball_y.append(p_tan[1])
            ball_z.append(p_tan[2])

    mlab.points3d(ball_x, ball_y, ball_z, np.ones(len(ball_x)), scale_factor=150,
                  color=(1,0.7,0.1))

    mlab.draw()

def draw_nucleus(v):
    mlab.clf()
    s = mlab.pipeline.triangular_mesh_source(x, y, z, triIndices)
    s.data.cell_data.scalars = np.cos(phaseAngle)
    surf = mlab.pipeline.surface(s)
    surf.contour.filled_contours = True
    surf.contour.minimum_contour = 0.0
    surf.contour.maximum_contour = 1.0
    surf.module_manager.scalar_lut_manager.data_range = (0,1)
    mlab.view(v)
    mlab.draw()

r_hat_virtis = np.array([0,0,1])
spice.furnsh("../input/spiceMetafile.tm")

# t = time for which the pointing is calculated
t = datetime.datetime(2015,4,25,0,28)
timeStamp = datetime.datetime.strftime(t, '%Y-%m-%dT%H:%M:%S')
et = spice.str2et(timeStamp)

# define virtis bore sight vector, first in instrument reference frame
# (which is [0,0,1]) and then rotate this vector into the comet centric
# frame of reference for the given time t.
rVirtis_hat = np.array([0,0,1])
R = spice.pxform('ROS_OSIRIS_NAC','67P/C-G_CK', et)
rVirtis_hat = np.dot(R, rVirtis_hat)
nPixelsX = 3
nPixelsY = 3
pVectors = pointing_vectors(nPixelsX, nPixelsY)

################################################################################
# compute coordinates of S/C and Sun in the comet body centric frame
m2km = 1000
observer = 'CHURYUMOV-GERASIMENKO'
corr = 'NONE'
frame = '67P/C-G_CK'
rSC, lt = spice.spkpos('ROSETTA', et, frame, corr, observer)
rSC = np.array(rSC, dtype=float) * m2km
rSC_hat = rSC / np.linalg.norm(rSC)

rSun, lt = spice.spkpos("SUN", et, frame, corr, observer)
rSun = np.array(rSun, dtype=float)
rSun_hat = rSun / np.linalg.norm(rSun)

rCG, lt = spice.spkpos("CHURYUMOV-GERASIMENKO", et, frame, corr, "ROSETTA")
rCG = np.array(rCG, dtype=float) * m2km
rCG_hat = rCG / np.linalg.norm(rCG)

################################################################################
# compute plotting coordinates
fStretch = np.linalg.norm(rSC)
center = np.zeros(3)
xSC_plt, ySC_plt, zSC_plt = plt_coords(center, rSC_hat*fStretch)
xSun_plt, ySun_plt, zSun_plt = plt_coords(center, rSun_hat*fStretch)
xVIR_plt, yVIR_plt, zVIR_plt = plt_coords(rSC_hat, rVirtis_hat*fStretch)

################################################################################
# load comet shape model and compute solar incident angles
fileName = '../input/shapeModel.ply'
fileName = '../input/SHAP5_stefano.ply'
nTriangles, nodeCoords, surfaceNormals, triIndices = load_shape_model_vtk(fileName)
x = nodeCoords[:,0]
y = nodeCoords[:,1]
z = nodeCoords[:,2]

phaseAngle = np.zeros(nTriangles)
for i in range(nTriangles):
  phaseAngle[i] = angle_between(rSun_hat, surfaceNormals[i])

################################################################################
# plot the results
# s and surf represent the nucleus shape model
# plot3d plots lines
figure = mlab.gcf()
figure.scene.interactor.add_observer('KeyPressEvent', hide_elements)

draw_scene()
mlab.show()
