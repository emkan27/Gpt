import argparse
import base64
import zlib


def encode_text(text: str) -> str:
    """Compress text with zlib and encode with URL-safe base64."""
    compressed = zlib.compress(text.encode("utf-8"))
    return base64.urlsafe_b64encode(compressed).decode("ascii")


def decode_text(encoded: str) -> str:
    """Decode URL-safe base64 text and decompress with zlib."""
    data = base64.urlsafe_b64decode(encoded)
    return zlib.decompress(data).decode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Encode or decode text")
    subparsers = parser.add_subparsers(dest="command", required=True)

    encode_parser = subparsers.add_parser("encode", help="Compress and encode text")
    encode_parser.add_argument("text", help="Text to encode")

    decode_parser = subparsers.add_parser("decode", help="Decode and decompress text")
    decode_parser.add_argument("data", help="Encoded text to decode")

    args = parser.parse_args()

    if args.command == "encode":
        print(encode_text(args.text))
    else:
        print(decode_text(args.data))


if __name__ == "__main__":
    main()
