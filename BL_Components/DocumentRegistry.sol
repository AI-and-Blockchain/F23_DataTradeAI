// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DocumentRegistry {
    struct Document {
        address owner;
        string ipfsHash;
    }

    mapping(string => Document) public documents;
    string public latestIPFSHash;

    event DocumentUploaded(address indexed owner, string ipfsHash);

    function uploadIPFSHash(string memory ipfsHash) public {
        require(documents[ipfsHash].owner == address(0), "Document already exists");
        documents[ipfsHash] = Document(msg.sender, ipfsHash);
        latestIPFSHash = ipfsHash; // Update latest IPFS hash
        emit DocumentUploaded(msg.sender, ipfsHash);
    }

    function getLatestIPFSHash() public view returns (string memory) {
        require(bytes(latestIPFSHash).length > 0, "No documents uploaded");
        return latestIPFSHash;
    }
}