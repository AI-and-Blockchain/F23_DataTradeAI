// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IPFSStorage {

    event HashStored(address indexed user, string hash);

    struct File {
        address owner;
        string ipfsHash;
    }

    mapping(uint256 => File) public files;
    uint256 public fileCount;

    function storeHash(string memory _ipfsHash) public {
        require(bytes(_ipfsHash).length > 0, "IPFS hash cannot be empty");
        
        files[fileCount] = File(msg.sender, _ipfsHash);
        fileCount++;
        
        emit HashStored(msg.sender, _ipfsHash);
    }
}