// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
/// @notice Stores vote receipt hashes only. Never store voter identity or ballot choices here.
contract VotingLedger {
    address public owner;
    mapping(bytes32 => bool) public recorded;
    event VoteReceiptAnchored(bytes32 indexed receiptHash, uint256 indexed electionId, uint256 timestamp);
    modifier onlyOwner(){ require(msg.sender == owner, "Only administrator"); _; }
    constructor(){ owner=msg.sender; }
    function anchorReceipt(bytes32 receiptHash, uint256 electionId) external onlyOwner {
        require(!recorded[receiptHash], "Receipt already anchored");
        recorded[receiptHash]=true;
        emit VoteReceiptAnchored(receiptHash,electionId,block.timestamp);
    }
}
