import numpy as np
import wave

# np.set_printoptions(threshold=100)

fileNameInput = 'knock'
FileOutPutName = 'work1.wav'


def runningMeanFast(x, N):
    """ x == an array of data. /n == number of samples per average """
    return np.convolve(x, np.ones(N) / N)


def unPackStringUsingWave(wavFile):
    """> write only the first name of the file, the program ill read it as wav like
    >unPackBinaryUsingWave("rocksong")
    >return sound_data, samplingfreq
    Returns wav-sound file in np.array format
    Spits two variables out : sound_data, samplingfreq
    sound_data      :  is the Array
    samplingfreq    :  is the Sampling Frequency of the wav file"""
    wav_name = f'{wavFile}.wav'
    read_wav = wave.open(f'{wav_name}', 'rb')
    samplingFreq = read_wav.getframerate()
    ampWidth = read_wav.getsampwidth()
    nFrames = read_wav.getnframes()
    compType = read_wav.getcomptype()
    compName = read_wav.getcompname()
    nChannel = read_wav.getnchannels()
    sound_Array = read_wav.readframes(read_wav.getnframes())

    sound_Array = np.array(wave.struct.unpack("%dh" % (len(sound_Array) / 2), sound_Array), dtype=np.int16)
    read_wav.close()
    sound_Array.shape = (nFrames, 2)  # Vi shaper ny array efter længde af sound_Array og sætter 2 colums i hele array
    sound_Array = sound_Array.T
    # print(sound_Array = sound_Array.T)
    return sound_Array, samplingFreq, ampWidth, nFrames, compType, compName, nChannel


def createLowPass(sound_Array, samplingFreq, ampWidth, nFrames, compType, compName, cutOffFrequency):

    # [1] ER FORDI VI GERNE VIL HAVE DET I EN CHANNEL SÅ LYDEN KOMMER I MONO MEN BLIVER AFSPILLET MAGAISK NOK I STEORO
    filtered = runningMeanFast(sound_Array[1], cutOffFrequency).astype(
        sound_Array.dtype)  # Retunere orginalt float f .astype(sound_Array.dtype)

    wav_file = wave.open(FileOutPutName, "w")
    wav_file.setparams((1, ampWidth, samplingFreq, nFrames, compType, compName))
    wav_file.writeframes(filtered.tobytes('C'))
    wav_file.close()

