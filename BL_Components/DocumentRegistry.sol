// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DocumentRegistry {
    struct Document {
        address owner;
        string ipfsHash;
    }

    mapping(string => Document) public documents;
    string[] internal hash_;
    string public latestIPFSHash;

    event DocumentUploaded(address indexed owner, string ipfsHash);
    event DataSent(string newDoc, string[] allDocs, uint256 modelOutput);
    event ModelOutputReceived(uint256 modelOutput, string ipfsHash);

    function uploadIPFSHash(string memory ipfsHash) public {
        require(documents[ipfsHash].owner == address(0), "Document already exists");
        emit DataSent(ipfsHash, hash_, 0);
    }
    
    function recOutput(uint256 _modelOutput, string calldata ipfsHash) external {
        emit ModelOutputReceived(_modelOutput, ipfsHash);
        require(_modelOutput != 1, "Document is plagiarized and cannot be accepted.");
        
        documents[ipfsHash] = Document(msg.sender, ipfsHash);
        hash_.push(ipfsHash);
        latestIPFSHash = ipfsHash; // Update latest IPFS hash
        emit DocumentUploaded(msg.sender, ipfsHash);


    }

    function getLatestIPFSHash() public view returns (string memory) {
        require(bytes(latestIPFSHash).length > 0, "No documents uploaded");
        return latestIPFSHash;
    }
}