from numpy import *

def pointing_vectors(nPixelsX=2, nPixelsY=2):
    phiX = 3.6669 / 2
    phiY = 3.6669 / 2
    iFOV = 0.00025
    PixelSize = 1
    InstrumentFrame = 'ROS_VIRTIS-M'
    lx = 2 * sin(phiX / 180.0 * pi)
    ly = 2 * sin(phiY / 180.0 * pi)

    rPointing = ones((3, nPixelsX,  nPixelsY))
    z = 1.0
    k = 1
    for (j,y) in enumerate(linspace(-ly/2.0, ly/2.0, nPixelsY)):
      for (i,x) in enumerate(linspace(-lx/2.0, lx/2.0, nPixelsX)):
        norm_rPointing = sqrt(x*x + y*y + z*z)
        rPointing[0,i,j] = x / norm_rPointing
        rPointing[1,i,j] = y / norm_rPointing
        rPointing[2,i,j] = z / norm_rPointing
        k += 1

    return rPointing
