import asyncio
import json
import requests
from web3 import Web3
from websockets import connect
import time
import sys
import re

ws_url = 'ws://127.0.0.1:8546'
rpc_url = 'http://localhost:8545'
w3 = Web3(Web3.HTTPProvider(rpc_url))


def gey():
    async def get_event():
        async with connect(ws_url) as ws:
            await ws.send('{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}')
            subscription_response = await ws.recv()
            response = json.loads(subscription_response)
            txHash = response['result']

            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=15)
                    response = json.loads(message)
                    if response['params']['result'] != txHash:
                        txHash = response['params']['result']
                        # filter and process the event data here
                        tx = w3.eth.get_transaction(txHash)
                        data = tx.input
                        fr = tx['from']
                        reg = r'^0x60a06040|^0x60806040'
                        track = r'04b04213c2774f77e60702880654206b116d00508|051e46fddf884518d96ebea18023f7b2d0a82582a|05b8a969814aea42cc1fac408e95383eb5c44e059|09bb69e4ddda0a1865fec3ba828787e6f886750f7|01717afbe81bb09cbd283f18474349efe2c27dced'
                        contract = re.findall(reg, data)
                        if contract:
                            findtrack = re.findall(track, data)
                            if findtrack:
                                print('generator :'+'\n'+'https://bscscan.com/tx/'+txHash)
                except Exception as e:
                    pass

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(get_event())
    except Exception as e:
        pass

gey()
