from wave import open as open_wave
import numpy as np
from pydub import AudioSegment
sound = AudioSegment.from_mp3("./AudioFiles/test.mp3")
wav = sound.export("./AudioFiles/test.mp3", format="wav")
fileWave = open_wave(wav,'rb') 
wframes = fileWave.getwframes() 
waveFrames = fileWave.readframes(wframes) 
waveData = np.fromstring(waveFrames, dtype=np.int16) 
