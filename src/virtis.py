from numpy import *

def pointing_vectors(nPixelsX=2, nPixelsY=2):
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

    if nPixelsX > 1:
        Dx = Lx / (nPixelsX - 1)
    else:
        Dx = Lx

    if nPixelsY > 1:
        Dy = Ly / (nPixelsY - 1)
    else:
        Dy = Ly

    r[0] = ii*Dx - Lx/2 + Dx/2
    r[1] = jj*Dy - Ly/2 + Dy/2
    r[2] = ones((len(i), len(j)))
    r_hat = r #/ (r[0]**2 + r[1]**2 + r[2]**2)

    return r_hat
