from web3 import Web3
import ipfshttpclient
from preprocessing import preprocess
import pickle
import numpy as np
import pandas as pd

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/621e6514991e48c5bfc09930b9e09c6e')) 
current_gas_price = web3.eth.gas_price
print(f"Current Gas Price: {current_gas_price} wei")

# Set the contract addresses
ml_contract_address = '0xF00Ff2148B4AAd677909cF9721310501C74eb388'
sender_account = '0x01f6fFa903e598C62a93092Bba5599367EfEfa4f'

nonce = web3.eth.get_transaction_count(sender_account)

ml_contract_abi = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "inputData",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "modelOutput",
				"type": "uint256"
			}
		],
		"name": "DataReceived",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "inputData",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "modelOutput",
				"type": "uint256"
			}
		],
		"name": "DataSent",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "modelOutput",
				"type": "uint256"
			}
		],
		"name": "ModelOutputReceived",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_modelOutput",
				"type": "uint256"
			}
		],
		"name": "recOutput",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "inputData",
				"type": "uint256"
			}
		],
		"name": "sendInput",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
ml_contract = web3.eth.contract(address=web3.to_checksum_address(ml_contract_address), abi=ml_contract_abi)

def send(model_result, hash):
    # Build transaction
    transaction = ml_contract.functions.recOutput(model_result, hash).buildTransaction({
        'from': sender_account,
        'gas': 200000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': web3.eth.getTransactionCount(sender_account),
    })

    # Sign and send transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, 'private_key')
    tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return tx_hash

def receive():
    event_filter = ml_contract.events.DataSent.create_filter(fromBlock='latest')
    event_filter.get_all_entries()
    while True:
        event_logs = ml_contract.events.DataSent.get_logs(fromBlock=0)
        print(event_logs)
        for event in event_filter.get_new_entries():
            print("yasss")
            received_data = event['args']['inputData']
            print(f"Received data from Oracle: {received_data}")
            '''try:
                hashs = list(request.args.getlist('hash_list'))
                documents = []
                for hash in hashs: #retrieve documents
                    documents.append(get_doc(hash))
                sus_document = str(get_doc(request.args.get('doc_hash')))
                model = pickle.load(open('./trained_models/decision_tree.sav', 'rb'))
                #data processing for model
                sus = np.array([sus_document]*len(documents)).reshape(-1,1)
                clas = np.array([-1]*len(documents)).reshape(-1,1)
                documents = np.array(documents).reshape(-1,1)
                d = np.concatenate([documents,sus,clas],axis = 1)
                data = pd.DataFrame(d, columns = ['Phrase','Suspicious','Class'])
                X,_,_ = preprocess(data)
                prediction = sum(model.predict(X))
                send(prediction, hash)
            except Exception as e:
                print(f"Error: {e}")
                return str(-1)'''

#Get from ipfs
def get_doc(ipfs_hash):
    try:
        client = ipfshttpclient.connect('ipfs address')

        response = client.cat(ipfs_hash)

        text_data = response.decode('utf-8')

        return text_data

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    receive()
