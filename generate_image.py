import spectral
import numpy as np
import scipy.misc

def scale_values(OldValue, OldMax, OldMin):
    """
    OldValue: The average value calculated across the BAND
    OldMin: The default Min value (-50.0)
    OldRange: The OldValue - (-50.0)
    """
    OldRange = (OldMax - OldMin) 
    NewRange = 256
    if(OldRange == 0.0):
        return 0
    else:
        NewValue = (((OldValue - OldMin) * NewRange) / OldRange)
        return int(NewValue)


image = spectral.envi.open('prm20120724t221057_rdn_ort.hdr', image='prm20120724t221057_rdn_ort')
fwhm = np.array([float(i) for i in open('fwhm.txt').read().strip().split(' , ')], dtype=np.float32)
wavelength = [float(i) for i in open('wavelength.txt').read().strip().split(' , ')]
IMAGE = []
IMAGE = np.zeros((1000, image.shape[1], 3), dtype=np.uint8)
for LINES in range(1000):
    MIN = 50.0
    MAX = 0.0
    for SAMPLES in range(image.shape[1]):
        #Array of values containing radiance spectrum
        BANDS = image[LINES,SAMPLES]
        min_val = min(BANDS)
        max_val = max(BANDS)
                    
        #Average across the spectra to retrieve values for RGB
        BLUE_LOWER = wavelength.index(0.4494496579)

        BLUE_HIGHER = wavelength.index(0.4947720080)

        GREEN_LOWER = wavelength.index(0.4976051329)

        GREEN_HIGHER = wavelength.index(0.5684515339)

        RED_LOWER = wavelength.index(0.6223183070)

        RED_HIGHER = wavelength.index(0.7499784920)

        RED = np.average(BANDS[RED_LOWER:RED_HIGHER])

        #fwhm_red = np.average(fwhm[RED_LOWER:RED_HIGHER])

        RED = scale_values(RED, min_val, max_val)

        BLUE = np.average(BANDS[BLUE_LOWER:BLUE_HIGHER])

        #fwhm_blue = np.average(fwhm[BLUE_LOWER:BLUE_HIGHER])

        BLUE = scale_values(BLUE, min_val, max_val)

        GREEN = np.average(BANDS[GREEN_LOWER:GREEN_HIGHER])

        #fwhm_green = np.average(fwhm[GREEN_LOWER:GREEN_HIGHER])

        GREEN = scale_values(GREEN, min_val, max_val)

        IMAGE[LINES][SAMPLES][0] = RED
        IMAGE[LINES][SAMPLES][1] = GREEN
        IMAGE[LINES][SAMPLES][2] = BLUE
