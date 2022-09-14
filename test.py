# %%
import walletTracker as wt
import time
from Tracker import walletTracker
# %%
wallets = {'FUBRMGmBd4YQ4wCvtF1aJ2Qt8EDSY8mH2fprTE6F7r2e',
           'BvKDnbsCgrJGADhCoKY8az5c8qhvFHPYaEekucmHsWqH', '3zby9bvaVyPMbggqstk2KUttzWrQXZVCqkW3mESRpfHk'}
trackers = []
previousAddress = {}
for wallet in wallets:
    previousAddress[wallet] = wt.test(wallet)
    trackers.append(walletTracker(wallet, previousAddress[wallet]))
# %%
for i in range(len(trackers)):
    trackers[i].previousAddress = wt.start(trackers[i].wallet,
                                           trackers[i].previousAddress)
# %%
print(wt.start(trackers[0].wallet, trackers[0].previousAddress))

# %%
