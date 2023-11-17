pragma solidity ^0.8.0;

contract DocumentRegistry {
    struct Document {
        address owner;
        string ipfsHash;
    }

    mapping(string => Document) public documents;

    event DocumentUploaded(address indexed owner, string ipfsHash);

    function uploadDocument(string memory ipfsHash) public {
        require(documents[ipfsHash].owner == address(0), "Document already exists");
        documents[ipfsHash] = Document(msg.sender, ipfsHash);
        emit DocumentUploaded(msg.sender, ipfsHash);
    }
}