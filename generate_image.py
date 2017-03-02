import spectral
import numpy as np
import scipy.misc

def scale_values(OldValue, OldRange):
    """
    OldValue: The average value calculated across the BAND
    OldMin: The default Min value (-50.0)
    OldRange: The OldValue - (-50.0)
    """
    OldMin = -50.0
    NewRange = 256
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) 
    return NewValue

image = spectral.envi.open('prm20120724t221057_rdn_ort.hdr', image='prm20120724t221057_rdn_ort')
fwhm = np.array([float(i) for i in open('fwhm.txt').read().strip().split(' , ')], dtype=np.float32)
IMAGE = []
IMAGE = np.zeros((1000, image.shape[1], 3), dtype=np.float32)
for LINES in range(1000):
    LINE = []
    for SAMPLES in range(image.shape[1]):
        #Array of values containing radiance spectrum
        BANDS = image[LINES,SAMPLES]
        #Average across the spectra to retrieve values for RGB
        
        #BLUE_LOWER = BANDS.index('0.3814931280')
        BLUE_LOWER = 0
        #BLUE_HIGHER = BANDS.index('0.4947720080')
        BLUE_HIGHER = 94

        #GREEN_LOWER = BANDS.index('0.4976051329')
        GREEN_LOWER = 95
        #GREEN_HIGHER = BANDS.index('0.6194827075')
        GREEN_HIGHER = 189

        #RED_LOWER = BANDS.index('0.6223183070')
        RED_LOWER = 190
        #RED_HIGHER = BANDS.index('0.7499784920')
        RED_HIGHER = 284


        RED = np.average(BANDS[RED_LOWER:RED_HIGHER])

        fwhm_red = np.average(fwhm[RED_LOWER:RED_HIGHER])

        RED = scale_values(RED, fwhm_red)

        BLUE = np.average(BANDS[BLUE_LOWER:BLUE_HIGHER])

        fwhm_blue = np.average(fwhm[BLUE_LOWER:BLUE_HIGHER])

        BLUE = scale_values(BLUE, fwhm_blue)

        GREEN = np.average(BANDS[GREEN_LOWER:GREEN_HIGHER])

        fwhm_green = np.average(fwhm[GREEN_LOWER:GREEN_HIGHER])

        GREEN = scale_values(GREEN, fwhm_green)

        #PIXEL_VALUE = [RED,BLUE,GREEN]

        IMAGE[LINES][SAMPLES][0] = RED
        IMAGE[LINES][SAMPLES][1] = GREEN
        IMAGE[LINES][SAMPLES][2] = BLUE
