## SecureScholar AI

A system for uploading academic papers to a permissionless blockchain, ensuring decentralization. An AI plagiarism detector verifies originality, and papers are published using IPFS, promoting academic integrity, secure document sharing, and a decentralized approach to data storage.

### Blockchain Architecture​
```
IPFS approach will be used for storing documents ​

Documents will be converted to a hash with SHA-256 before uploads and a self-executing smart contract with the hash will be deployed on the blockchain​

The blockchain will then check if the document sets off any flags for plagiarism in a proactive manner​

Once verified and added to the blockchain, the actual document will be stored on a decentralized storage solution (IPFS)​

Documents can be retrieved by anyone with access rights by using the hash in the smart contract ​
```

## ML pipeline
![ML pipeline](/Diagrams/ML_pipeline.PNG?raw=true "ML pipeling")

## Sequence Diagram
![Sequence Diagram](/Diagrams/SequenceDiagram.png?raw=true "Sequence Diagram")

