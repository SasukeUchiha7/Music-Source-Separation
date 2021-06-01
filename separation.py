import torch
import torchaudio
import numpy as np
import scipy 
# import stempeg
import os
import youtube_dl
from scipy.io.wavfile import read, write
import wave
import soundfile as sf
from openunmix import predict

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
data,fs = sf.read ('test.wav')

estimates = predict.separate(
    torch.as_tensor(data).float(),
    rate=fs,
    device=device
)   
for target, estimate in estimates.items():
    print(target)
    audio = estimate.detach().cpu().numpy()[0]
    write(target+'.wav',fs,data)
