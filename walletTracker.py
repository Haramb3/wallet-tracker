import requests
import pandas as pd
import json
from discord_webhook import DiscordWebhook, DiscordEmbed


def requestJson(walletToTrack):
    headers = {
        'authority': 'beta.api.solanalysis.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.6',
        # Already added when you pass json=
        # 'content-type': 'application/json',
        'origin': 'https://hyperspace.xyz',
        'referer': 'https://hyperspace.xyz/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    json_data = {
        'operationName': 'GetUserMPAHistory',
        'variables': {
            'condition': {
                'buyer_address': walletToTrack,
                'seller_address': None,
                'by_mpa_types': [
                    'TRANSACTION',
                ],
            },
            'order_by': {
                'field_name': 'block_timestamp',
                'sort_order': 'DESC',
            },
            'pagination_info': {
                'page_number': 1,
                'page_size': 30,
                'progressive_load': True,
            },
        },
        'query': 'query GetUserMPAHistory($condition: GetMarketPlaceActionsByUserCondition!, $order_by: [OrderConfig!], $pagination_info: MPAPaginationConfig) {\n  getUserHistory(\n    condition: $condition\n    order_by: $order_by\n    pagination_info: $pagination_info\n  ) {\n    market_place_snapshots {\n      token_address\n      project_id\n      project_name\n      name\n      owner\n      full_img\n      rank_est\n      moonrank\n      howrare_rank\n      meta_data_img\n      is_project_verified\n      market_place_state {\n        marketplace_program_id\n        marketplace_instance_id\n        type\n        price\n        block_timestamp\n        seller_address\n        seller_referral_address\n        seller_referral_fee\n        signature\n        escrow_address\n        buyer_address\n        buyer_referral_address\n        buyer_referral_fee\n        created_at\n        metadata\n        token_address\n        __typename\n      }\n      __typename\n    }\n    pagination_info {\n      current_page_number\n      current_page_size\n      has_next_page\n      __typename\n    }\n    __typename\n  }\n}',
    }
    response = requests.post(
        'https://beta.api.solanalysis.com/graphql', headers=headers, json=json_data)
    data = response.json()
    dictionary = data['data']['getUserHistory']['market_place_snapshots']
    df = pd.DataFrame.from_dict(dictionary)
    return df


def checkForNewBuy(wallet, previousAddress):
    df = requestJson(wallet)
    if df['token_address'][0] == previousAddress:
        return False, None, previousAddress
    else:
        previousAddress = df['token_address'][0]
        return True, df, previousAddress


def createWebhook(df):
    url = "https://discord.com/api/webhooks/1019444725306101850/g56rjoqTQNWufyOzSqUC2iZ91VP-C1nz3dPtZoqaHYLx_UXRN1ZcQfPhqjMTT_2VjKar"
    webhook = DiscordWebhook(url=url, username='Wallet Tracker')
    embed = DiscordEmbed(
        description="Price: " + str(df['market_place_state'][0]['price']) + "",
        title=str(df['project_name'][0])
    )
    embed.set_image(url=str(df['meta_data_img'][0]))
    embed.add_embed_field(
        name='Link', value="https://hyperspace.xyz/token/"+str(df['token_address'][0])+"")
    webhook.add_embed(embed)
    response = webhook.execute()


def start(wallet, previousAddress):
    df = requestJson(wallet)
    check, df2, prevAddress = checkForNewBuy(wallet, previousAddress)
    if check:
        createWebhook(df2)
    else:
        pass
    return prevAddress


def test(address):
    df = requestJson(address)
    createWebhook(df)
    return df['token_address'][0]
