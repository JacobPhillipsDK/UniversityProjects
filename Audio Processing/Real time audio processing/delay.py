import numpy as np
import scipy.io.wavfile as wave


#The code has been inspired by Aalborg University, Mads Græsbøll Christensen, Audio Analysis Lab.Lecture 8: Audio Effects. Mar. 25, 2021

soundStringInput = '../lydfiler/reverse_reverb2.wav' #input string
soundStringOutput = '../lydfiler/reverse_reverb3.wav' #output string
normalize = True
Scaled = True
Flip1 = True
Flip2 = True


samplingFreq, xSignal = wave.read(soundStringInput)
if normalize:
    xSignal = xSignal[:, 0] / 2 ** 15  # normalise
if Flip1:
    xSignal =np.flip(xSignal)

def combfiltering(inputSignal, filterCoef, delay, feedBackIsUsed=True):
    nData = np.size(inputSignal)
    outputSignal = np.zeros(nData)
    for n in np.arange(nData):
        if n < delay:
            outputSignal[n] = inputSignal[n]
        else:
            if feedBackIsUsed:
                outputSignal[n] = inputSignal[n]+filterCoef*outputSignal[n-delay]
            else:
                outputSignal[n] = inputSignal[n]+filterCoef*inputSignal[n-delay]
    return outputSignal

filterCoef = 0.8
delay = np.int(np.round(0.15*samplingFreq)) # samples
feedBackIsUsed = True
delay_signal = combfiltering(xSignal, filterCoef, delay, feedBackIsUsed)

if Flip2:
    delay_signal = np.flip(delay_signal)

if Scaled:
    scaled = np.int16(delay_signal / np.max(np.abs(delay_signal)) * 32767)  # Makes audio file playable in 16 bit
    print("Scaled succesfully")
    wave.write(soundStringOutput, samplingFreq, scaled)
else:
    wave.write(soundStringOutput, samplingFreq, delay_signal)
    print("Did not scale")



