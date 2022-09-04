# DO NOT SHARE THIS FILE (shown here as an example for this project)
# It contains your wallet's address and private key

myAddress = "B6j1joj71UbkwEMnt1AJt5AzyWvMFr3BuN"
myPrivateKey = "KzvkfzM1maN9JNnQ4K2BajeYYiwWDpidnuZ8MrDKsck2DRHVnxm6"
rpcUser = "bcs_tester"
rpcPassword = "iLoveBCS"
rpcIp = "45.32.232.25"
rpcPort = "3669"

def getMyAddress():
    '''Returns your personal wallet's address.'''
    return myAddress

def getMyKey():
    '''Returns your personal wallet's private key.'''
    return myPrivateKey

def getRpcValues():
    '''Returns values needed for JSONRPC call in a form of tuple. 
    Returned tuple: (rpcUser, rpcPassword, rpcIp, rpcPort)
    '''
    return (rpcUser, rpcPassword, rpcIp, rpcPort)
