import torch
import torchaudio
import numpy as np
import scipy 
from openunmix import predict
import audiofile as af

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")

def separateMusic(source):
    data,fs = af.read(source)
    track = np.copy(data)
    estimates = predict.separate(
        torch.as_tensor(track).float(),
        rate=fs,
        device=device
    )   
    for target, estimate in estimates.items():
        print(target)
        audio = estimate.detach().cpu().numpy()[0]
        af.write('static/sounds/'+target+'.wav',audio,fs)
