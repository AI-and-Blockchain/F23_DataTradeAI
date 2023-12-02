const Web3 = require('web3');
const contractAddress = "0xd9145CCE52D386f254917e481eB44e9943F39138"; // Replace with the actual deployed contract address
import contractAbi from '../contract.abi.json'

// Create an instance of web3 using the injected provider (e.g., MetaMask)
const web3 = new Web3(window.ethereum);

// Create a contract instance using the contract address and ABI
const ssaContract = new web3.eth.Contract(contractAbi, contractAddress);

// Temp IPFS Hash
const IPFSHash = "tmp"

// Function to upload a file to IPFS with Helia
async function uploadFile() {
  try {
    // Call the 'uploadIPFSHash' function of the smart contract
    await ssaContract.methods.uploadIPFSHash(IPFSHash).send({ from: web3.eth.defaultAccount });

    const documentContent = await ssaContract.methods.getLatestIPFSHash().call();
    const contentDisplay = document.querySelector(`ftext`);
    contentDisplay.textContent = `${documentContent} votes`;
  } catch (error) {
    console.error(error);
  }
}
  async function uploadInitFile() {
    try {
      // Call the 'uploadInitDocs' function of the smart contract
      await ssaContract.methods.uploadInitDocs(IPFSHash).send({ from: web3.eth.defaultAccount });
  
      const documentContent = await ssaContract.methods.getLatestIPFSHash().call();
      const contentDisplay = document.querySelector(`ftext`);
      contentDisplay.textContent = `${documentContent} votes`;
    } catch (error) {
      console.error(error);
    }
}