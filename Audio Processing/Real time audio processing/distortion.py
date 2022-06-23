import numpy as np
import scipy.signal as sig
import scipy.io.wavfile as wave

soundStringInput = '../lydfiler/music_of_life.wav'  # input string
soundStringOutput = '../lydfiler/distortion.wav'  # output string
normalize = True
Scaled = True

samplingFreq, xSignal = wave.read(soundStringInput)

if normalize:
    xSignal = xSignal[:,0] / 2 ** 15  # normalise

def distortion( inputSignal, filterCoef,samplingFreq, trigger): #plain filter
    nData = np.size(inputSignal) #gets length of inputsignal
    outputSignal = np.zeros(nData) #zeropadding
    for n in np.arange(nData):
        if (np.int((n*filterCoef/samplingFreq)) % trigger) == 0:
            # print(np.int((n * filterCoef / samplingFreq)))
            # print(np.int((n*filterCoef/samplingFreq)) % trigger)
            # print(n)
            continue
        else:
            outputSignal[n] = inputSignal[n]
    return outputSignal

trigger = 5 # trigger for distortion
filterCoef = 200 # Samples trigger value +1
xSignal=distortion(xSignal, filterCoef,samplingFreq,trigger)


if Scaled:
    scaled = np.int16(xSignal / np.max(np.abs(xSignal)) * 32767)  # Makes audio file playable in 16 bit
    wave.write(soundStringOutput, samplingFreq, scaled)
    print("Sclaed")
else:
    wave.write(soundStringOutput, samplingFreq, xSignal)
    print("Did not scale")