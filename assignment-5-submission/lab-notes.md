# Assignment 5 — Lab Notes

## Lab 1: Setup
- Commands executed:
  - `build/bin/bitcoind -regtest -daemon`
  - `build/bin/bitcoin-cli -regtest createwallet devwallet` (failed - wallet existed)
  - `build/bin/bitcoin-cli -regtest loadwallet devwallet`
  - `build/bin/bitcoin-cli -regtest generatetoaddress 101 $ADDRESS`
- Output observed:
  - Initial blockchain height: 101 blocks
  - After mining: 202 blocks with verificationprogress=1
  - Wallet address: bcrt1qg90n57j7g4ruz5erynv56hfhfma9wf8sv6mtuc
- Key insight: Regtest mode requires generating initial blocks to make coins spendable. First 101 blocks (including coinbase maturity) needed before transactions.

## Lab 2: Multi-Node Network
- Commands executed:
  - Created second node with `-datadir=$HOME/bitcoin-node2`
  - Configured with port=19444, rpcport=19443
  - `build/bin/bitcoin-cli -regtest addnode "127.0.0.1:19444" onetry`
- Peers connected: 1 peer connected (127.0.0.1:19444)
- Key insight: Each node needs unique ports for P2P and RPC. The node displayed "Unable to bind" errors when ports conflicted with the first node.

## Lab 3: Mempool
- TXID: `70b1f3e4b1a844410384f8bc896d7b4b3e85547a8da5a7a3305d67ce8833bac6`
- Mempool size before mine: 1 transaction, size=141 bytes, fee=0.00001410 BTC
- Key insight: Unconfirmed transactions remain in mempool until mined. After generating a block, confirmations increased to 1.

## Lab 4: Compact Blocks (BIP152)
- Messages observed: No compact block messages captured during testing
- Key insight: Compact blocks (cmpctblock) reduce bandwidth by sending only short transaction IDs. Nodes can reconstruct blocks from mempool, enabling faster propagation.

## Lab 5: Compact Filters (BIP157/158)
- Filter header for block 1: `f86347aace87a920c43a4023bf295f8626439371c88f9eeae0a835f8bf1b6d79`
- Block 1 hash: `09b8eecada4cf7ea30e99f97d6113eb40269c9c3f5a439b6361a2df28e229095`
- Key insight: Compact filters enable lightweight clients to download only relevant blocks without compromising privacy. The filter `019cafa0` represents the block's transaction set.

## Lab 6: Merkle Tree
- Block hash: `70369300a992e683d74c5f2f5e9e4ca9d218257c9a75524eed26ce983114bb90`
- Merkle root: `10eb493152520e7acef9ab35b669621d5f90b51679c4f1ac01fa5cf7f40f2476`
- Computed root matches: yes (verification script confirmed)
- Key insight: Merkle roots allow SPV clients to verify transactions belong to a block without downloading the full block. Single transaction blocks produce merkle root matching the txid.

## Lab 7: Bloom Filters (BIP37)
- False positive rate: 0.1% configured (1000 capacity, error_rate=0.001)
- Privacy problem: Bloom filters reveal which data the client is watching. An adversary can analyze filter patterns to determine wallet addresses, linking transactions to the same client.

## Lab 8: Consensus Rules
- What happened when the block was corrupted: No corruption errors appeared in debug.log because the corrupted file was in the backup copy, not the active blocks directory. The node didn't detect or reject it since it wasn't loaded.
- Key insight: Bitcoin nodes validate each block's proof-of-work, merkle root, and transaction signatures. Corrupted blocks are rejected and banned peers are disconnected.

## Lab 9: Peer Connections
- Number of peers: 1
- Protocol version: 70016
- Services advertised: NETWORK, WITNESS, NETWORK_LIMITED, P2P_V2
- Peer details: `127.0.0.1:19444`, software version `/Satoshi:31.99.0/`, inbound=false
