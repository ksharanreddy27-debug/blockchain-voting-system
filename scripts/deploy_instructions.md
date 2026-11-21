# Optional Ethereum test-network integration

The Django demo runs without a blockchain node and maintains a local SHA-256-linked audit ledger. To anchor receipt hashes on Ethereum, use a local development chain only (Hardhat or Ganache), compile and deploy `contracts/VotingLedger.sol`, and retain the deployed address and ABI. Do not use a public chain or real election data.

1. Start a local chain on `http://127.0.0.1:8545`.
2. Compile/deploy `VotingLedger.sol` using Remix connected to the local chain, or your preferred Hardhat setup.
3. Copy the contract address into `.env` as `VOTING_CONTRACT_ADDRESS` and set `WEB3_PROVIDER_URI`.
4. Set `WEB3_FROM_ADDRESS` to the address of an unlocked local test account in your local node. The Django app uses the node's unlocked-account transaction facility. Never use this setting with a real account or public network.

The app submits `anchorReceipt(bytes32,uint256)` transactions when all three environment settings are present and the local node exposes the test account as unlocked. The local hash-chain feature is active by default regardless.
