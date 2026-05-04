import hashlib
import subprocess
import json

def double_sha256(b: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def build_merkle_root(txids: list) -> str:
    hashes = [bytes.fromhex(txid)[::-1] for txid in txids]
    while len(hashes) > 1:
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])
        hashes = [double_sha256(hashes[i] + hashes[i+1])
                  for i in range(0, len(hashes), 2)]
    return hashes[0][::-1].hex()

def main():
    CLI = "/home/livingproof/bitcoin/build/bin/bitcoin-cli"

    result = subprocess.run([CLI, "-regtest", "getbestblockhash"],
                            capture_output=True, text=True)
    block_hash = result.stdout.strip()

    result = subprocess.run([CLI, "-regtest", "getblock", block_hash, "1"],
                            capture_output=True, text=True)
    block = json.loads(result.stdout)

    txids = block["tx"]
    expected_root = block["merkleroot"]
    computed_root = build_merkle_root(txids)

    print(f"Block hash:     {block_hash}")
    print(f"Expected root:  {expected_root}")
    print(f"Computed root:  {computed_root}")
    print(f"Match: {expected_root == computed_root}")

if __name__ == "__main__":
    main()
