import matplotlib.pyplot as plt
import pandas as pd
import math
from pandas import Series, DataFrame
import sys


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100): 
    formatStr = "0:." + str(decimals) + "f" 
    percent = formatStr.format(100 * (iteration / float(total))) 
    filledLength = int(round(barLength * iteration / float(total))) 
    bar = '#' * filledLength + '-' * (barLength - filledLength) 
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)), 
    if iteration == total: 
        sys.stdout.write('\n') 
    sys.stdout.flush()


def iat2(y, x):
    return (((y*32+(x/2))/x)*2)  # 3.39 mxdiff

def AOA_iatan2sc(y, x):
    # determine octant
    if (y >= 0):    # oct 0,1,2,3
        if (x >= 0):  # oct 0,1
            if (x > y): 
                return iat2(-y, -x)/2 + 0*32
            else:
                if (y == 0):
                    return 0 # (x=0,y=0)
            return (-iat2(-x, -y)/2 + 2*32)

        else:  # oct 2,3
        # if (-x <= y) 
            if (x >= -y): 
                return (iat2(x, -y)/2 + 2*32)
            else: 
                return (-iat2(-y, x)/2 + 4*32)

    else:  # oct 4,5,6,7
        if (x < 0):  # oct 4,5
            # if (-x > -y) 
            if (x < y) :
                return (iat2(y, x)/2 + -4*32)
            else:
                return (-iat2(x, y)/2 + -2*32)
        
        else:  # oct 6,7
        # if (x <= -y) 
            if (-x >= y): 
                return (iat2(-x, y)/2 + -2*32)
            else: 
                return (-iat2(y, -x)/2 + -0*32)


def AOA_AngleComplexProductComp(Xre, Xim, Yre, Yim):
    Zre, Zim = int(0)
    angle = int(0)

    # X*conj(Y)
    Zre = Xre*Yre + Xim*Yim
    Zim = Xim*Yre - Xre*Yim

    # Angle. The angle is returned in 256/2*pi format [-128,127] values
    angle = AOA_iatan2sc(int(Zim), int(Zre))

    return (angle * angleconst)


typedef struct
{
  int16_t i;  //!< I - In-phase
  int16_t q;  //!< Q - Quadrature
} AoA_IQSample_Ext_t;

typedef struct
{
  int8_t i;  //!< I - In-phase
  int8_t q;  //!< Q - Quadrature
} AoA_IQSample_t;


def AOA_getPairAngles(AoA_AntennaConfig_t *antConfig, AoA_AntennaResult_t *antResult, uint16_t numIqSamples, uint8_t sampleRate, uint8_t sampleSize, uint8_t slotDuration, uint8_t numAnt, int8_t *pIQ)
{
    # IQ Samples can be 32 bit per sample or 16 bit per sample (where each sample is normalized to 8 bits)
    AoA_IQSample_Ext_t *pIQExt
    AoA_IQSample_t *pIQNorm

    Paa_rel = 0
    Pab_rel = 0
    secondIQfactor = 1 # in slot duration of 1 usec, there are 180 degrees between adjacent antennas samples so the factor will be -1

    numPairs = 3 # 무조건 3

    # Average relative angle across repetitions
    antenna_versus_avg = [[0 for col in range(6)] for row in range(6)]
    antenna_versus_cnt = [[0 for col in range(6)] for row in range(6)]

    for (uint16_t r = 1; r < (numIqSamples - (8*sampleRate))/(numAnt*sampleRate) ; ++r) # Sample Slot
    {
    for (uint16_t i = 0; i < sampleRate; ++i) # Sample inside Sample Slot
    {
      # Loop through antenna pairs and calculate phase difference
      for (uint8_t pair = 0; pair < numPairs; ++pair)
      {
        const AoA_AntennaPair_t *p = &antConfig->pairs[pair];
        uint8_t a = p->a; # First antenna in pair
        uint8_t b = p->b; # Second antenna in pair

        # In slot duration of 1 usec, there are 180 degrees between adjacent antennas samples
        if (slotDuration == AOA_SLOT_DURATION_1US)
        {
          if ((abs(a-b) % 2) == 1)
          {
            secondIQfactor = -1; # in slot duration of 1 usec, there are 180 degrees between adjacent antennas samples,
                                 # because the antenna switch is in the middle of the sine wave period
          }
        }

        if (sampleSize == 1)
        {
          pIQNorm = (AoA_IQSample_t *)pIQ;

          # Calculate the phase drift across one antenna repetition (X * complex conjugate (Y))
          Paa_rel = AOA_AngleComplexProductComp(pIQNorm[8*sampleRate + r*numAnt*sampleRate + a*sampleRate + i].i,
                                                pIQNorm[8*sampleRate + r*numAnt*sampleRate + a*sampleRate + i].q,
                                                pIQNorm[8*sampleRate + (r-1)*numAnt*sampleRate + a*sampleRate + i].i * secondIQfactor,
                                                pIQNorm[8*sampleRate + (r-1)*numAnt*sampleRate + a*sampleRate + i].q * secondIQfactor);

          # Calculate phase difference between antenna a vs. antenna b
          Pab_rel = AOA_AngleComplexProductComp(pIQNorm[8*sampleRate + r*numAnt*sampleRate + a*sampleRate + i].i,
                                                pIQNorm[8*sampleRate + r*numAnt*sampleRate + a*sampleRate + i].q,
                                                pIQNorm[8*sampleRate + r*numAnt*sampleRate + b*sampleRate + i].i * secondIQfactor,
                                                pIQNorm[8*sampleRate + r*numAnt*sampleRate + b*sampleRate + i].q * secondIQfactor);
        }
        else # sampleSize == 2
        {
          pIQExt = (AoA_IQSample_Ext_t *)pIQ;

          # Calculate the phase drift across one antenna repetition (X * complex conjugate (Y))
          Paa_rel = AOA_AngleComplexProductComp(pIQExt[8*sampleRate + r*numAnt*sampleRate + a*sampleRate + i].i,
                                                pIQExt[8*sampleRate + r*numAnt*sampleRate + a*sampleRate + i].q,
                                                pIQExt[8*sampleRate + (r-1)*numAnt*sampleRate + a*sampleRate + i].i * secondIQfactor,
                                                pIQExt[8*sampleRate + (r-1)*numAnt*sampleRate + a*sampleRate + i].q * secondIQfactor);

          # Calculate phase difference between antenna a vs. antenna b
          Pab_rel = AOA_AngleComplexProductComp(pIQExt[8*sampleRate + r*numAnt*sampleRate + a*sampleRate + i].i,
                                                pIQExt[8*sampleRate + r*numAnt*sampleRate + a*sampleRate + i].q,
                                                pIQExt[8*sampleRate + r*numAnt*sampleRate + b*sampleRate + i].i * secondIQfactor,
                                                pIQExt[8*sampleRate + r*numAnt*sampleRate + b*sampleRate + i].q * secondIQfactor);
        }


        # Add to averages
        # v-- Correct for angle drift / ADC sampling frequency error
        antenna_versus_avg[a][b] += Pab_rel + ((Paa_rel * abs(a-b)) / numAnt);
        antenna_versus_cnt[a][b] ++;
      }
    }
    }

    # Calculate the average relative angles
    for (int i = 0; i < numAnt; ++i)
    {
    for (int j = 0; j < numAnt; ++j)
    {
      antenna_versus_avg[i][j] /= antenna_versus_cnt[i][j];
    }
    }

    # Write back result for antenna pairs
    for (uint8_t pair = 0; pair < numPairs; ++pair)
    {
    AoA_AntennaPair_t *p = &antConfig->pairs[pair];
    antResult->pairAngle[pair] = (int)((p->sign * antenna_versus_avg[p->a][p->b] + p->offset) * p->gain);
    }
}

if __name__ == "__main__":

    print('test start!')
    file_name = input("enter_file_name:")
    file_name += '.csv'

    df = pd.read_csv(file_name)



    grouped = df
    grouped[['i', 'q']].plot(title="I/Q samples", grid=True)
    
    plt.show()

