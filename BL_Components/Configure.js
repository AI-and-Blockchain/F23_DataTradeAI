// This JavaScript code uses the ipfs-http-client library to add a file to IPFS and returns the IPFS hash, which you can then pass to the smart contract's storeHash function.
// Requies: npm install ipfs-http-client

const IPFS = require('ipfs-http-client');
const ipfs = IPFS.create({ host: 'ipfs.infura.io', port: 5001, protocol: 'https' });

const addFileToIPFS = async (fileContent) => {
  const fileAdded = await ipfs.add(fileContent);
  return fileAdded.cid.toString();
};

// Example usage
const fileContent = 'data.txt';
addFileToIPFS(fileContent).then(ipfsHash => {
  console.log(`IPFS Hash: ${ipfsHash}`);
});