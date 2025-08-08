# verifier.py
import os
import torch
import torchaudio
import numpy as np
from speechbrain.pretrained import SpeakerRecognition

ENROLL_PATH = "data/enroll.wav"

class VoiceVerifier:
    def __init__(self, enroll_path=ENROLL_PATH):
        self.verifier = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa")
        self.enroll_path = enroll_path
        if not os.path.exists(enroll_path):
            raise FileNotFoundError(f"Enrollment file not found at {enroll_path}. Run enroll.py first.")
        self.enroll_embedding = self._get_embedding(enroll_path)

    def _get_embedding(self, wav_path):
        # returns embedding tensor
        emb = self.verifier.encode_batch(wav_path)
        # emb is tensor [1, emb_dim]
        return emb.squeeze(0)

    def verify(self, test_wav_path, threshold=0.65):
        """Return (is_same, score) where score is cosine similarity"""
        test_emb = self._get_embedding(test_wav_path)
        # cosine similarity
        cos = torch.nn.functional.cosine_similarity(self.enroll_embedding.unsqueeze(0), test_emb.unsqueeze(0)).item()
        return (cos >= threshold, cos)
