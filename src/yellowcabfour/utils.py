"""Utility functions."""

import os
import pickle
from typing import Any

def save_pickle(obj: Any, filename: str) -> None:
    """Save object as pickle file."""
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def load_pickle(filename: str) -> Any:
    """Load object from pickle file."""
    with open(filename, 'rb') as f:
        return pickle.load(f) 