from pycoin.coins.bitcoin.Tx import Tx
from pycoin.encoding.hexbytes import h2b, h2b_rev
from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.tx_utils import create_tx, sign_tx

import requests, sys
from hidden import getMyKey, getMyAddress, getRpcValues
from .models import Transaction

# Utils functions for views.py


def buildSpendable(utxo):
    '''
    Gets JSON utxo data and returns 
    a Spendable object instance.
    '''
    value = utxo['value']
    script = utxo['scriptPubKey']
    tx_id = utxo['transactionId']
    outputIndex = utxo['outputIndex']

    # print('value:', value, '\nscript:', script, 
    #             '\ntx_id:', tx_id, '\noutputIndex:', outputIndex)

    # print('SCRIPT:', script)
    # script_bytes = unhexlify(script)
    # print('SCRIPT BYTES:', script.encode())

    # script_bytes = script.encode()
    # tx_id_bytes = tx_id.encode()
    # print(script_bytes) # -- FOR DEBUG

    spendable = Tx.Spendable(
        coin_value=int(value), 
        script=h2b(script), 
        tx_hash=h2b_rev(tx_id),
        tx_out_index=outputIndex
    )
    print('***\n', spendable.coin_value, 
        spendable.script, 
        spendable.tx_hash,
        spendable.tx_out_index)
    print('***')

    return spendable


def getBcsUtxo():
    '''
    Function to get UTXO for the given address 
    from API.
    '''

    base_url = 'https://bcschain.info/api/address/{}/utxo/'

    # Try to connect; throw an error if unsuccessful
    try:
        api_url = base_url.format(getMyAddress())
        # print('URL:', api_url) # -- FOR DEBUG
        response = requests.get(api_url)
    except:
        print("Error: ", sys.exc_info())
        quit()

    return response.json()[0]


def getRecipientAddress():
    '''
    Returns a recipient's address gotten through JSONRPC response.
    '''

    rpcValues = getRpcValues()
    rpcUser = rpcValues[0]
    rpcPass = rpcValues[1]
    rpcIp = rpcValues[2]
    rpcPort = rpcValues[3]

    # Get new recipient's address
    try:
        rpcUrl = "http://" + rpcUser + ":" + rpcPass + "@" + rpcIp + ":" + rpcPort + '/wallet/'
        response = requests.post(rpcUrl, json={'jsonrpc':'2.0', 'method':'getnewaddress', 'id':'test'})
    except:
        print("Error: ", sys.exc_info())
        quit()

    return response.json()['result']
    

def sendTx(signed_tx):
    '''
    Gets hex representation of a signed transaction 
    and sends it to a JSONRPC server.

    Returns a JSON reponse from a request.
    '''

    rpcValues = getRpcValues()
    rpcUser = rpcValues[0]
    rpcPass = rpcValues[1]
    rpcIp = rpcValues[2]
    rpcPort = rpcValues[3]

    try:
        rpcUrl = "http://" + rpcUser + ":" + rpcPass + "@" + rpcIp + ":" + rpcPort
        # print(rpcUrl) # -- FOR DEBUG
        json_data = {'jsonrpc':'2.0', 'method':'sendrawtransaction','params':['{}'.format(signed_tx)], 'id': 'testnet'}
        # print('JSON:', json_data) # -- FOR DEBUG
        response = requests.post(rpcUrl, json=json_data)
    except:
        print("Error: ", sys.exc_info())
        quit()

    return response.json()


def makeTx():
    '''
    Perform all the necessary steps to send a transaction. 
    
    Return JSON response with tx's number, error code and id. 

    Example: {'result': 'tx_number_here', 'error': None, 'id': 'your_id_here'}
    '''

    # Step 1 -- Get an address to send coins to
    recipientAddress = getRecipientAddress()

    # Step 2 -- Create and sign a transaction

    # Create a network with given parameters
    bcs_network = create_bitcoinish_network(
        symbol="", network_name="", subnet_name="", 
        wif_prefix_hex="80", address_prefix_hex="19", pay_to_script_prefix_hex="32", 
        bip32_prv_prefix_hex="0488ade4", bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc",  # bip32 parameters
        bip49_prv_prefix_hex="049d7878", bip49_pub_prefix_hex="049D7CB2",                   # bip49 parameters
        bip84_prv_prefix_hex="04b2430c", bip84_pub_prefix_hex="04B24746",                   # bip 84 parameter
        magic_header_hex="F1CFA6D3", default_port=3666
    )

    # Needed arguments for performing a transaction
    senderAddress = getMyAddress()
    satoshi = 100000000 # Amount of satoshi needed for 1 BCS coin; 1e8 = 1 BCS coin
    spendable = buildSpendable(getBcsUtxo())
    payables = [(recipientAddress, satoshi), (senderAddress)]
    wifs = [getMyKey()]

    # Create a transaction
    tx = create_tx(network=bcs_network, 
                    spendables=[spendable], 
                    payables=payables, 
                    fee = 90500)
    # Sign the created transaction
    sign_tx(network=bcs_network, tx=tx, wifs=wifs)


    # Step 3 -- Get tx's hex representation, 
    # send it and get a JSON response
    tx_hex = tx.as_hex()
    tx_response = sendTx(tx_hex)

    return tx_response
