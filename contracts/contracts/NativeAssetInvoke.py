import binascii
import sys

from boa.interop.Ontology.Native import Invoke
from boa.builtins import ToScriptHash, state
from boa.interop.System.Runtime import Notify
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash


# ONT Big endian Script Hash: 0x0100000000000000000000000000000000000000
OntContract = ToScriptHash("AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV")
# ONG Big endian Script Hash: 0x0200000000000000000000000000000000000000
OngContract = ToScriptHash("AFmseVrdL9f9oyCzZefL9tG6UbvhfRZMHJ")


selfContractAddress = GetExecutingScriptHash()

def Main(operation, args):
    if operation == "transferOntOng":
        if len(args) == 4:
            fromAcct = args[0]
            toAcct = args[1]
            ontAmount = args[2]
            ongAmount = args[3]
            return transferOntOng(fromAcct, toAcct, ontAmount, ongAmount)
        else:
            return False
    if operation == "transferOngToContract":
        if len(args) == 2:
            fromAccount = args[0]
            ongAmount = args[1]
            return transferOngToContract(fromAccount, ongAmount)
        else:
            return False
    if operation == "checkSelfContractONGAmount":
        return checkSelfContractONGAmount()
    return False

def transferOntOng(fromAcct, toAcct, ontAmount, ongAmount):
    param = state(fromAcct, toAcct, ontAmount, ongAmount)
    res = Invoke(0, OntContract, "transfer", [param])
    if res != b'\x01':
        raise Exception("transfer ont error.")
    param = state(fromAcct, toAcct, ongAmount)
    Notify("transferONT succeed")
    res = Invoke(0, OngContract, "transfer", [param])
    if res != b'\x01':
        raise Exception("transfer ong error.")
    Notify("transferONG succeed")
    return True


def transferOngToContract(fromAccount, ongAmount):
    Notify(["111_transferOngToContract", selfContractAddress])
    param = state(fromAccount, selfContractAddress, ongAmount)
    res = Invoke(0, OngContract, 'transfer', [param])
    if res and res == b'\x01':
        Notify('transfer Ong succeed')
        return True
    else:
        Notify('transfer Ong failed')
        return False


def checkSelfContractONGAmount():
    param = state(selfContractAddress)
    # do not use [param]
    res = Invoke(0, OngContract, 'balanceOf', param)
    return res


if __name__ == "__main__":
#     # "sc-compile": "python contracts/ontsctf.py -c contracts/contracts/ExchangeContract.cs",
#     # "sc-deploy": "python contracts/ontsctf.py -m contracts/config/deploy.json",
#     # "sc-invoke": "python contracts/ontsctf.py -i contracts/config/invoke.json"
#     test = True
#     # args = ['-c', 'contracts/ExchangeContract.cs']
#     # args = ['-m', 'config/deploy.json']
#     # args = ['-i', 'config/invoke.json']
    addrfrom = binascii.hexlify(b"ANXq3ezHTFvUhYZBComEHxXiJ3bSLAU7ek")
    addrto = binascii.hexlify(b"AN27EevbmnmDJ6nqQU6eJR17wvNbHkc1P8")
    #414e587133657a485446765568595a42436f6d45487858694a3362534c415537656b
    #414e587133657a485446765568595a42436f6d45487858694a3362534c415537656b

    print(addrfrom, addrto)
#     args = [addrfrom, addrto, 0, 112]
#     if test:
#         Main("transferOntOng", args)
#     else:
#         print(sys.argv)
#         # Main(sys.argv[1:])
