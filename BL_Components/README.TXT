IPFS Storage
- Prerequisites: run npm install to download dependencies from package.json and then run npm start
- Use node app.js to run a demo for storing a file to an IPFS filesystem from a local IPFS node

Smart Contract are responsible for:
- Storing hashes of the text documents
- Providing a list of users who can use the documents
- Interact with IPFS and ML code to detect plagarism text
- Returns to user the hash of their text document if storing on the IPFS was successful, else returns plagarism detected