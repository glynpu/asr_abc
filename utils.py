#!/usr/bin/env python3
# Copyright 2021 Xiaomi Corporation (Author: Liyong Guo)

import os
import logging
from pathlib import Path
from huggingface_hub import list_repo_files, hf_hub_download
from typing import Dict, List


class AttributeDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise AttributeError(f"No such attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        if key in self:
            del self[key]
            return
        raise AttributeError(f"No such attribute '{key}'")


def download_models(repo: str, model_files: List[str], cache_root: Path):
    available_files = list_repo_files(repo)
    for f in model_files:
        assert f in available_files
        f = Path(f)
        cache_dir = cache_root / f
        Path(os.path.dirname(f)).mkdir(parents=True, exist_ok=True)
        logging.info(f"About to download {f} if doesn't exist.")
        cache_path = hf_hub_download(repo, f, cache_dir=cache_dir)
        os.system(f"ln -sf {cache_path} {f}")


def load_dict(dict_path: Path) -> Dict[int, str]:
    ret = {}
    with open(dict_path) as f:
        for line in f:
            word, idx = line.strip().split()
            assert idx not in ret
            idx = int(idx)
            ret[idx] = word

    return ret


def remove_repeated_and_leq(labels, blank=0):
    new_labels = []
    # remove consecutive duplicate indexes
    previous = None
    for ll in labels:
        if ll != previous:
            new_labels.append(ll)
            previous = ll
    # remove blank
    new_labels = [ll for ll in new_labels if ll > blank]
    return new_labels


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    download_models()
