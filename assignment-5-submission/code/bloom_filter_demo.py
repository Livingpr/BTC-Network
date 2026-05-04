from pybloom_live import BloomFilter
import subprocess, json

CLI = "/home/livingproof/bitcoin/build/bin/bitcoin-cli"

# Create a filter that holds 1000 items with 0.1% false-positive rate
bf = BloomFilter(capacity=1000, error_rate=0.001)

# Get some real txids from our regtest chain
result = subprocess.run(
    [CLI, "-regtest", "getrawmempool"],
    capture_output=True, text=True)
mempool_txids = json.loads(result.stdout)

# Add txids to the filter
test_txids = ["abc123fake", "def456fake"] + mempool_txids[:3]
for txid in test_txids:
    bf.add(txid)
    print(f"Added: {txid[:20]}...")

print()
print(f"'abc123fake' in filter: {'abc123fake' in bf}")
print(f"'notinthere' in filter: {'notinthere' in bf}  (should be False)")
print()
print("NOTE: BIP37 bloom filters are deprecated in Bitcoin Core")
print("due to privacy leaks — clients reveal which transactions")
print("they are watching. BIP158 compact filters replaced them.")
