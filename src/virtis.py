from numpy import *

def pointing_vectors():
    nPixelsX = 256
    nPixelsY = 256
    PhiX = 3.6669 / 2
    PhiY = 3.6669 / 2
    iFOV = 0.00025
    PixelSize = 1
    InstrumentFrame = 'ROS_VIRTIS-M'

    Lx = 2 * sin(PhiX / 180 * pi)
    Ly = 2 * sin(PhiY / 180 * pi)

    i = arange(nPixelsX)
    j = arange(nPixelsY)
    ii, jj = meshgrid(i, j, indexing='ij')
    r = array([zeros((len(i), len(j))) for k in range(3)])

    r[0] = ii*Dx - Lx/2 + Dx/2
    r[1] = jj*Dy - Ly/2 + Dy/2
    r[2] = ones((len(i), len(j)))
    #r_hat = r / sqrt(r[0]**2 + r[1]**2 + r[2]**2)
    r_hat = r / norm(r)

    return r_hat
