#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


from src.encoder import encode, decode, Metadata, StepMeta


def main():
    parser = argparse.ArgumentParser(description="Encode or decode messages")
    subparsers = parser.add_subparsers(dest="command")

    enc_parser = subparsers.add_parser("encode", help="Encode a message")
    enc_parser.add_argument("message", help="Message to encode")
    enc_parser.add_argument("--meta", help="Path to write metadata", default=None)

    dec_parser = subparsers.add_parser("decode", help="Decode a message")
    dec_parser.add_argument("encoded", help="Encoded message")
    dec_parser.add_argument("metadata", help="Path to metadata JSON file")

    args = parser.parse_args()

    if args.command == "encode":
        encoded, meta = encode(args.message)
        print(encoded)
        if args.meta:
            Path(args.meta).write_text(json.dumps(meta, default=lambda o: o.__dict__, indent=2))
    elif args.command == "decode":
        data = json.loads(Path(args.metadata).read_text())
        steps = [StepMeta(name=s['name'], params=s['params']) for s in data['steps']]
        meta = Metadata(steps=steps)
        print(decode(args.encoded, meta))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
