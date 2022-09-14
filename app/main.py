from flask import Flask
import walletTracker as wt
import time
from Tracker import walletTracker

app = Flask(__name__)

wallets = {'FUBRMGmBd4YQ4wCvtF1aJ2Qt8EDSY8mH2fprTE6F7r2e',  # President
           'BvKDnbsCgrJGADhCoKY8az5c8qhvFHPYaEekucmHsWqH',
           '3zby9bvaVyPMbggqstk2KUttzWrQXZVCqkW3mESRpfHk',  # Clement
           'BP9a7nk1GJFAeLDJL1BxnXDRxzJviHT66w6Qcznz3t1X',
           'fr7YFkGeJNGMxVJAhQgp9gZivKSNPcQU4roBK4boKGB',  # SolanaGodess
           '3AEqNkS6T7ig535rbMc7oDV6uavL2KF3zRGAPbtj5Ngc',  # Tominator
           'GRhe2vLFj6e2pzPA1fmi3ZaMM7ZiwD36VLvGGYjoXEkz',  # Gav
           }
trackers = []
previousAddress = {}
for wallet in wallets:
    previousAddress[wallet] = wt.test(wallet)
    trackers.append(walletTracker(wallet, previousAddress[wallet]))
print("Server is running...")


@app.route('/')
def main():
    print("Checking...")
    for i in range(len(trackers)):
        trackers[i].previousAddress = wt.start(trackers[i].wallet,
                                               trackers[i].previousAddress)
    # wt.test()    return "<h1>WALLET TRACKER IS WORKING...</h1>"
