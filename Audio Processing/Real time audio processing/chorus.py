import numpy as np
import scipy.signal as sig
import scipy.io.wavfile as wave

#The code has been inspired by Aalborg University, Mads Græsbøll Christensen, Audio Analysis Lab.Lecture 8: Audio Effects. Mar. 25, 2021

soundStringInput = '../lydfiler/music_of_life.wav' #input string
soundStringOutput = '../lydfiler/Vibrato.wav' #output string
normalize = True
Scaled = True
Vibrato = True
Chorus = False

samplingFreq, xSignal = wave.read(soundStringInput)

if normalize:
    xSignal = xSignal[:, 0] / 2 ** 15  # normalise

def addVibrato(inputSignal, modDepth, digModFreq, offset=0):
    #array for holding input
    nData = np.size(inputSignal)
    #Array for holding output
    outputSignal = np.zeros(nData)
    #Array for holding delay
    tmpSignal = np.zeros(nData)
    for n in np.arange(nData):
        # calculate delay by multiplying the depth with an oscilating sinusoid
        delay = offset + (modDepth/2)*(1-np.cos(digModFreq*n))
        # calculate filter output
        #if statement skal være der, fordi vi har variable delay, kan delay gå i minus under udregning, hvilket ikke
        #giver mening. Derfor sætter vi vores delay til 0 når n er mindre end vores delay.
        if n < delay:
            outputSignal[n] = 0
        else:
            intDelay = np.int(np.floor(delay))
            #Laver delayed signal som er vores inputSignals samples, minuset med delay.
            tmpSignal[n] = inputSignal[n-intDelay]
            fractionalDelay = delay-intDelay
            apParameter = (1-fractionalDelay)/(1+fractionalDelay)
            outputSignal[n] = apParameter*tmpSignal[n]+tmpSignal[n-1]-apParameter*outputSignal[n-1]
    return outputSignal


def addSinusoidalChorus(inputSignal, mixParam, offset, digModFreq, modDepth):
    # add the original instrument to the mix
    outputSignal = inputSignal
    # add additional instruments using the vibrato effect
    nAdditionInstruments = np.size(mixParam)
    for ii in np.arange(nAdditionInstruments):
        outputSignal = outputSignal + \
            mixParam[ii]*addVibrato(inputSignal, modDepth[ii], digModFreq[ii], offset[ii])
    return outputSignal



if Vibrato:
    maxDelay = 0.0005 * samplingFreq  # samples
    digModFreq = 2 * np.pi * 5 / samplingFreq  # rad/sample
    xSignal = addVibrato(xSignal,maxDelay,digModFreq)
    print ("Virbrato effect succesfully added")


if Chorus == True & Vibrato == False:
    mixParam = np.array([0.9, 0.9, 0.8])
    offset = np.array([0.01, 0.012, 0.008]) * samplingFreq  # samples
    digModFreq = 2 * np.pi * np.array([0.1, 0.15, 0.05]) / samplingFreq  # radians/sample
    modDepth = np.array([0.02, 0.021, 0.018]) * samplingFreq  # samples
    xSignal = addSinusoidalChorus(xSignal, mixParam, offset, digModFreq, modDepth)
    print("Chorus effect succesfully added")
else:
    print("Both Chorus and Vibrato is sat to true, only ran vibrato")


if  Scaled:
    scaled = np.int16(xSignal / np.max(np.abs(xSignal)) * 32767)  # Makes audio file playable in 16 bit
    wave.write(soundStringOutput, samplingFreq, scaled)
    print("Sclaed")
else:
    wave.write(soundStringOutput, samplingFreq, xSignal)
    print("Did not scale")