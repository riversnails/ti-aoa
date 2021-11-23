import matplotlib.pyplot as plt
import pandas as pd
import math

def cal_magnitude(q_value,i_value):

    return math.sqrt(math.pow(q_value,2)+math.pow(i_value,2))
    #return math.sqrt(math.pow(q_value,2)+math.pow(i_value,2))

def cal_phase(q_value,i_value):

    return math.degrees(math.atan2(q_value,i_value))

if __name__ == "__main__":
    df = pd.read_csv('sla_rtls_raw_iq_samples.csv')
    AOA_RES_MAX_SIZE=81

    # We only want one set of data per channel
    df = df.drop_duplicates(subset=['channel','sample_idx'] , keep='first')

    # We Calculate the phase and the margin
    df['phase'] = df.apply(lambda row: cal_phase(row['q'], row['i']), axis=1)
    df['magnitude'] = df.apply(lambda row: cal_magnitude(row['q'], row['i']), axis=1)

    # Plot all the I/Q collected. Each channel will have a plot which contains I/Q samples.
    # If you have collected I/Q data on 37 data channels, then there will be 37 windows popped up
    grouped = df.groupby('channel')
    grouped[['i', 'q']].plot(title="I/Q samples", grid=True)
    plt.show()

    # Create 4 plots and each plot has x number of subplots. x = number of channels
    '''indexed = df.set_index(['channel', 'sample_idx'])
    indexed.unstack(level=0)[['phase']].plot(subplots=True, title="Phase information", xlim=[0,AOA_RES_MAX_SIZE], ylim=[-190,+190])
    indexed.unstack(level=0)[['magnitude']].plot(subplots=True, title="Signal magnitude", xlim=[0,AOA_RES_MAX_SIZE])
    indexed.unstack(level=0)[['i']].plot(subplots=True, title="I samples", xlim=[0,AOA_RES_MAX_SIZE])
    indexed.unstack(level=0)[['q']].plot(subplots=True, title="Q samples", xlim=[0,AOA_RES_MAX_SIZE])
    plt.show()'''
