from nacl.signing import SigningKey
import base58
import json
from pathlib import Path

def generate_keypair(name, keypair_type):
    # Generate a new random signing keypair
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key

    # Get the seed and public key in bytes
    private_key_bytes = signing_key.encode()
    public_key_bytes = verify_key.encode()

    # Convert to base58
    private_key = base58.b58encode(private_key_bytes).decode('ascii')
    public_key = base58.b58encode(public_key_bytes).decode('ascii')

    # Create keypair JSON
    keypair = {
        "private": private_key,
        "public": public_key
    }

    # Save to file
    keypair_path = Path(__file__).parent / "keypairs" / f"{name}_{keypair_type}_keypair.json"
    with open(keypair_path, 'w') as f:
        json.dump(keypair, f, indent=2)

    return keypair_path

def main():
    # Generate keypairs for both workers
    for worker in ["worker1", "worker2"]:
        for keypair_type in ["staking", "public"]:
            path = generate_keypair(worker, keypair_type)
            print(f"Generated {keypair_type} keypair for {worker}: {path}")

if __name__ == "__main__":
    main() 