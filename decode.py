#!/usr/bin/env python3
# Copyright 2021 Xiaomi Corporation (Author: Liyong Guo)

import sys

import argparse
import os
import logging
from pathlib import Path

import torch
import torchaudio

from conformer import Conformer
from utils import load_dict, AttributeDict, remove_repeated_and_leq, download_models

sys.path.append("./lhotse")
from lhotse import Fbank, FbankConfig  # noqa: E402

REPO = "GuoLiyong/cn_conformer_encoder_aishell"
MODEL_FILES = [
    "data/lang_char/tokens.txt",
    "exp/conformer_encoder.pt",
]
CACHE_ROOT = "model_caches"

def get_params() -> AttributeDict:
    params = AttributeDict(
        {
            "sample_rate": 16000,
            # parameters for conformer
            "num_classes": 4336,
            "subsampling_factor": 4,
            "feature_dim": 80,
            "nhead": 4,
            "attention_dim": 512,
        }
    )
    return params


def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--model",
        type=Path,
        default="exp/conformer_encoder.pt",
        help="Model used to recognize wavs.",
    )

    parser.add_argument(
        "--token-path",
        type=Path,
        default="data/lang_char/tokens.txt",
        help="token dict used to recognize wavs.",
    )

    parser.add_argument(
        "--input-wav",
        "-i",
        type=Path,
        default="./data/wavs/BAC009S0764W0143.wav",
        help="Wav to be recognized.",
    )

    parser.add_argument(
        "--enable-debug",
        "-d",
        action="store_true",
        help="debug mode",
    )
    return parser


def main():
    formatter = (
        "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    )
    logging.basicConfig(format=formatter, level=logging.INFO)
    parser = get_parser()
    args = parser.parse_args()
    if not os.path.isfile(args.model):
        assert str(args.model) in MODEL_FILES, f"Inaccurate model name {args.model}"
        cache_root = Path(os.getcwd()) / CACHE_ROOT
        download_models(repo=REPO, model_files=MODEL_FILES, cache_root=cache_root)
    assert os.path.isfile(args.model)
    assert os.path.isfile(args.token_path)
    assert os.path.isfile(args.input_wav)
    logging.info("All files seem exist.")

    params = get_params()
    params.update(vars(args))

    logging.info("Start loading model.")
    model = Conformer(
        num_features=params.feature_dim,
        nhead=params.nhead,
        d_model=params.attention_dim,
        num_classes=params.num_classes,
        enable_debug=params.enable_debug,
    )
    checkpoint = torch.load(args.model, map_location="cpu")
    model.load_state_dict(checkpoint["model"], strict=True)

    device = torch.device("cpu")
    if torch.cuda.is_available():
        device = torch.device("cuda", 0)
    model.to(device)
    model.eval()

    logging.info("Start loading dict.")
    token_dict = load_dict(params.token_path)

    if params.enable_debug:
        import pdb; pdb.set_trace()

    logging.info(f"Start recognize {params.input_wav}.")
    audio_samples, sample_rate = torchaudio.load(params.input_wav)
    assert sample_rate == 16000, \
        f"sample_rate of {params.input_wav} is {sample_rate}," + \
        f"while 16000 is expected."
    fbank_extractor = Fbank(FbankConfig(num_mel_bins=80))
    features = fbank_extractor.extract(audio_samples, sample_rate)
    features = torch.tensor(features).to(device).unsqueeze(0)
    with torch.no_grad():
        nnet_output, memory = model(features)

    if params.enable_debug:
        import pdb; pdb.set_trace()
    token_ids = nnet_output.argmax(dim=2)
    token_ids = token_ids.cpu().squeeze().numpy()
    token_ids = remove_repeated_and_leq(token_ids)
    hyp = [token_dict[id] for id in token_ids]
    hyp = "".join(hyp)
    logging.info(f"Result: {hyp}")
    logging.info("done.")


if __name__ == "__main__":
    main()
