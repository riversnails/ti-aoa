import matplotlib.pyplot as plt
import pandas as pd
import math
from pandas import Series, DataFrame
import sys

def cal_magnitude(q_value,i_value):

    return math.sqrt(math.pow(q_value,2)+math.pow(i_value,2))

def cal_phase(q_value,i_value):

    return math.degrees(math.atan2(q_value,i_value))


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100): 
    formatStr = "{0:." + str(decimals) + "f}" 
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

    # X*conj(Y)
    Zre = Xre*Yre + Xim*Yim
    Zim = Xim*Yre - Xre*Yim

    # Angle. The angle is returned in 256/2*pi format [-128,127] values
    angle = AOA_iatan2sc(int(Zim), int(Zre))

    return (angle * (180/128))



if __name__ == "__main__":

    print('test start!')
    file_name = input("enter_file_name:")
    file_name += '.csv'

    df = pd.read_csv(file_name)
    #df = pd.read_csv('sla_rtls_raw_iq_samples.csv')

    AOA_RES_MAX_SIZE=81
    IDX_MAX = 623
    TIME_LENGTH = 8

    #그냥 처음받은 데이터만 분석하겠다는 말 데이터 다짤림 주의
    # We only want one set of data per channel
    # df = df.drop_duplicates(subset=['channel','sample_idx'] , keep='first')
    # print(df)

    # We Calculate the phase and the margin
    df['phase'] = df.apply(lambda row: cal_phase(row['q'], row['i']), axis=1)
    df['magnitude'] = df.apply(lambda row: cal_magnitude(row['q'], row['i']), axis=1)

    #df.to_csv("test_csv")

    # Plot all the I/Q collected. Each channel will have a plot which contains I/Q samples.
    # If you have collected I/Q data on 37 data channels, then there will be 37 windows popped up

    # grouped = df.groupby('channel')
    # grouped[['i', 'q']].plot(title="I/Q samples", grid=True)

    #채널분류없이 데이터 순서대로 나열된다. 위에 중복제거 막고 실행

    # grouped = df
    # grouped[['i', 'q']].plot(title="I/Q samples", grid=True)
    
    # plt.show()

    print('___degree_test_start___')

    print(df.columns)
    print(df.index)

    """df = df.groupby('ant_array')
                df[['i', 'q']].plot(title="I/Q samples", grid=True)
                plt.show()"""

    data = {
        'degree':[None]
    }

    degree_group = DataFrame(data)

    print(degree_group)

    length = len(df.index)
    print(length)

    """for i in range(1, length):
                    printProgress(i, length, 'Progress:', 'Complete', 1, 50)
                    Paa_rel = AOA_AngleComplexProductComp(df.iloc[i].i, df.iloc[i].q, df.iloc[i - 1].i, df.iloc[i - 1].q)
                    Pab_rel = AOA_AngleComplexProductComp(df.iloc[i].i, df.iloc[i].q, df.iloc[i].i, df.iloc[i].q)
                  
                    if df.iloc[i].ant_array == 1:
                        degree_group.loc[i] = ((Paa_rel + Pab_rel) / 2) #+ 45
                    else:
                        degree_group.loc[i] = ((Paa_rel + Pab_rel) / 2) #- 45"""

    """for i in range(0,TIME_LENGTH + 1) : # df 의 index 갯수만큼 반복
            
                    pluse_data = 0
            
                    for j in range(0, IDX_MAX + 1) :
                        printProgress(j, (IDX_MAX * 1), 'Progress:', 'Complete', 1, 50)
                        pluse_data = ((df.iloc[(IDX_MAX * i) + j].phase)) + pluse_data
            
            
                    degree_group.loc[i] = pluse_data / IDX_MAX
                    print(' data:')
                    print(pluse_data)
                    print(degree_group.loc[i])
            """
    
    
    print(degree_group)

    degree_group[['degree']].plot(title="test", grid=True)
    plt.show()

    print('___degree_test_end___')




    #df = df.drop_duplicates(subset=['channel','sample_idx'] , keep='first')
    print(df)
    # Create 4 plots and each plot has x number of subplots. x = number of channels
    #indexed = df.set_index(['pkt', 'sample_idx'])
    #indexed.unstack(level=0)[['phase']].plot(subplots=True, title="Phase information", xlim=[0,AOA_RES_MAX_SIZE], ylim=[-190,+190])
    #indexed.unstack(level=0)[['magnitude']].plot(subplots=True, title="Signal magnitude", xlim=[0,AOA_RES_MAX_SIZE])
    #indexed.unstack(level=0)[['i']].plot(subplots=True, title="I samples", xlim=[0,AOA_RES_MAX_SIZE])
    #indexed.unstack(level=0)[['q']].plot(subplots=True, title="Q samples", xlim=[0,AOA_RES_MAX_SIZE])

    df['phase'].plot(title="phase", grid=True)
    df['magnitude'].plot(title="magnitude", grid=True)
    plt.show()






    """for i in range(0,9) : # df 의 index 갯수만큼 반복
            
                    pluse_data = 0
            
                    for j in range(0, 623) :
                        printProgress(j, (623 * 1), 'Progress:', 'Complete', 1, 50)
                        pluse_data = df.iloc[(623 * i) + j].phase
            
            
                    degree_group.loc[i] = pluse_data / 623
                    print(' data:')
                    print(pluse_data)
                    print(degree_group.loc[i])"""

           #         """  if df.iloc[i].ant_array == 1:
            #                  degree_group.loc[i] = ((df.iloc[i].i + df.iloc[i].q) / 2) + 45
             #             else:
              #                degree_group.loc[i] = ((df.iloc[i].i + df.iloc[i].q) / 2) - 45"""