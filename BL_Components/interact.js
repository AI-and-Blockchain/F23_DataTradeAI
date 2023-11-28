const Web3 = require('web3');
const contractAddress = "0x42eFB830A90323f60c5767d91a50848f5D7804B5"; // Replace with the actual deployed contract address
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