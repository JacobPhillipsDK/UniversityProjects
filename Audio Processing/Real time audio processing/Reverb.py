import numpy as np
import scipy.io.wavfile as wave
import matplotlib.pyplot as plt  # used to plot signals.

#The code has been inspried by Aalborg University Mads Græsbøll Christensen Audio Analysis Lab.Lecture 8: Audio Effects. Mar. 25, 2021

soundStringInput = '../lydfiler/music_of_life.wav' #input string
soundStringOutput = '../lydfiler/reverse_reverb2.wav' #output string
Scaled = True
Flip1 = False
Flip2 = False


samplingFreq, xSignal = wave.read(soundStringInput) #read file
xSignal = xSignal[:, 0] / 2 ** 15  # normalise
if Flip1:
    xSignal = np.flip(xSignal)



def plainReverberator(inputSignal, delay, filterCoef,feedback=True): #plain filter
    nData = np.size(inputSignal) #gets length of inputsignal
    outputSignal = np.zeros(nData) #zeropadding
    for n in np.arange(nData):
        if n < delay:
            outputSignal[n] = inputSignal[n]
        else:
            if feedback:
                outputSignal[n] = inputSignal[n] + filterCoef * outputSignal[n - delay]  # y(n) = x(n)+ ay(n-d)
            else:
                # Feedforward comb filter
                outputSignal[n] = inputSignal[n] + filterCoef * inputSignal[n - delay]  # y(n) = x(n)+ ax(n-d)
    return outputSignal


def allpassReverberator(inputSignal, delay, filterCoef): #All-pass filter
    nData = np.size(inputSignal)
    outputSignal = np.zeros(nData)
    for n in np.arange(nData):
        if n < delay:
            outputSignal[n] = inputSignal[n]
        else:
            outputSignal[n] = \
                filterCoef * outputSignal[n - delay] - filterCoef * inputSignal[n] + inputSignal[n - delay]
            # y(n) = ay(n-d)-ax(n) + x(n-d)
    return outputSignal

def shroederReverb(inputSignal, plainMix, plainDelays, plainCoef, allpassDelays, allpassCoef):
    nData = np.size(inputSignal)
    outputSignal = np.zeros(nData) #zero padding
    # run the plain reverberators in parallel
    nPlainReverberators = np.size(plainDelays)
    for n in np.arange(nPlainReverberators):
        outputSignal = outputSignal + \
                    plainMix[n] * plainReverberator(inputSignal, plainDelays[n], plainCoef[n])
        print("plainfilter",n+1,"added")
    # run the allpass reverberators in series
    nAllpassReverberators = np.size(allpassDelays)
    for n in np.arange(nAllpassReverberators):
        outputSignal = allpassReverberator(outputSignal, allpassDelays[n], allpassCoef[n])
        print("allpass:",n+1,"added")
    return outputSignal

#plain filters param
mixPlain = np.array([0.2, 0.3, 0.25, 0.25]) #Filter co for plain filters
plainDelays = np.array([1553, 1613, 1493, 1153]) # delay frequency all has to be prime numbers
plainCoef = np.array([0.7, 0.7, 0.7, 0.7])  # a coefficient

#allpass filters params
allpassDelays = np.array([223, 443])  # delay frequency all has to be prime numbers
allpassCoef = np.array([0.7, 0.7])  # Filter co for plain filters


if np.sum(mixPlain) != 1:
    print(np.sum(mixPlain))
    print("wrong parameter and is not equal 1")

elif (np.size(plainDelays) != np.size(mixPlain)):
    print("arrays of plain filters is not equal size")
elif (np.size(allpassDelays)!= np.size(allpassCoef)):
    print("array of allpass filters is not equal size")
else:

    signalWithReverb = \
    shroederReverb(xSignal, mixPlain, plainDelays, plainCoef, allpassDelays, allpassCoef) #creates signal
    if Flip2:
        signalWithReverb = np.flip(signalWithReverb) #re-flips audio
        print ("flipped audio")
    if Scaled:
        scaled = np.int16(signalWithReverb / np.max(np.abs(signalWithReverb)) * 32767) #Makes audio file playable in 16 bit
        scaled1 = np.int16(xSignal / np.max(np.abs(xSignal)) * 32767)  # Makes audio file playable in 16 bit
        print(np.max(np.abs(signalWithReverb)))
        wave.write(soundStringOutput, samplingFreq, scaled) #compute the audio file
        print("Scaled succesfully")
    else:
        wave.write(soundStringOutput, samplingFreq, signalWithReverb) #compute the audio file
        print("Did not scale output")

    plt.figure("reverb")
    plt.plot(scaled1, label="Reverb", color = "green")
    # plt.plot(xSignal, label ="Original", color = "orange")
    plt.xlabel("Sample index")
    plt.ylabel("Amplitude")
    plt.title("Waveform reverse reverb vs original")
    plt.legend()

    plt.figure("Reverb")
    plt.plot(xSignal, label ="Original", color = "orange")
    plt.xlabel("Sample index")
    plt.ylabel("Amplitude")
    plt.title("Waveform reverse reverb vs original")
    plt.legend()
    plt.show()