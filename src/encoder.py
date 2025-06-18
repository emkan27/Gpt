import base64
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

# Define available transformations

def _caesar_shift(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if 'a' <= ch <= 'z':
            base = ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        elif 'A' <= ch <= 'Z':
            base = ord('A')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

def _caesar_unshift(text: str, shift: int) -> str:
    return _caesar_shift(text, -shift)


def _xor(text: str, key: int) -> str:
    return ''.join(chr(ord(ch) ^ key) for ch in text)


def _substitute(text: str, mapping: Dict[str, str]) -> str:
    return ''.join(mapping.get(ch, ch) for ch in text)

def _reverse_substitute(text: str, mapping: Dict[str, str]) -> str:
    rev = {v: k for k, v in mapping.items()}
    return ''.join(rev.get(ch, ch) for ch in text)


def _base64_encode(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def _base64_decode(text: str) -> str:
    return base64.b64decode(text.encode()).decode()


TRANSFORMATIONS = {
    'caesar': (_caesar_shift, _caesar_unshift),
    'xor': (_xor, _xor),  # XOR is symmetric
    'substitution': (_substitute, _reverse_substitute),
    'base64': (_base64_encode, _base64_decode),
}

@dataclass
class StepMeta:
    name: str
    params: Dict[str, Any]


@dataclass
class Metadata:
    steps: List[StepMeta]


def encode(message: str) -> Tuple[str, Metadata]:
    """Apply random transformations to the message.

    Returns the encoded message and metadata needed to reverse it.
    """
    available = list(TRANSFORMATIONS.keys())
    num_steps = random.randint(1, len(available))
    steps = random.sample(available, num_steps)

    meta_steps = []
    encoded = message
    for step in steps:
        if step == 'caesar':
            shift = random.randint(1, 25)
            encoded = TRANSFORMATIONS[step][0](encoded, shift)
            meta_steps.append(StepMeta(name=step, params={'shift': shift}))
        elif step == 'xor':
            key = random.randint(1, 255)
            encoded = TRANSFORMATIONS[step][0](encoded, key)
            meta_steps.append(StepMeta(name=step, params={'key': key}))
        elif step == 'substitution':
            letters = [chr(i) for i in range(32, 127)]
            shuffled = letters[:]
            random.shuffle(shuffled)
            mapping = dict(zip(letters, shuffled))
            encoded = TRANSFORMATIONS[step][0](encoded, mapping)
            meta_steps.append(StepMeta(name=step, params={'mapping': mapping}))
        elif step == 'base64':
            encoded = TRANSFORMATIONS[step][0](encoded)
            meta_steps.append(StepMeta(name=step, params={}))
        else:
            raise ValueError(f'Unknown step {step}')
    metadata = Metadata(steps=meta_steps)
    return encoded, metadata


def decode(encoded_text: str, metadata: Metadata) -> str:
    """Reverse the encoding using metadata."""
    decoded = encoded_text
    for step in reversed(metadata.steps):
        name = step.name
        params = step.params
        transform = TRANSFORMATIONS[name][1]
        if name == 'caesar':
            decoded = transform(decoded, params['shift'])
        elif name == 'xor':
            decoded = transform(decoded, params['key'])
        elif name == 'substitution':
            decoded = transform(decoded, params['mapping'])
        elif name == 'base64':
            decoded = transform(decoded)
        else:
            raise ValueError(f'Unknown step {name}')
    return decoded

