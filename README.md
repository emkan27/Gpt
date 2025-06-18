# Gpt

## Encoder CLI

This repository provides an example encoder/decoder that chains random reversible
transformations. The CLI is located at `scripts/run_encode.py`.

```
./scripts/run_encode.py encode "Hello" --meta meta.json
./scripts/run_encode.py decode <encoded> meta.json
```

### Available Transformations

* **Caesar shift** – shifts alphabetical characters by a random amount.
* **XOR** – applies a byte-wise XOR with a random integer key.
* **Substitution** – substitutes printable ASCII characters using a random mapping.
* **Base64** – encodes or decodes using Base64.

### Extending

Add a new transformation by updating `src/encoder.py`:

1. Implement a pair of functions for encode/decode.
2. Register them in `TRANSFORMATIONS` with a unique name.
3. Include any random parameters in the metadata so `decode` can reverse them.

