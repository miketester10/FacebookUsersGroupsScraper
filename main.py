import time
import pandas as pd
import requests

id_gruppo = input('Inserisci ID gruppo Facebook: ')
next_page_flag = True
utenti = []

variables = {"count":10,"id":f"{id_gruppo}","scale":1.5}

while next_page_flag:

    url = "https://www.facebook.com/api/graphql/"

    headers = { 

        'Accept-Encoding': 'json',
        # cambiare Cookie se cambi account Facebook
        'Cookie': '',
        'Sec-Fetch-Site': 'same-origin',
        'X-FB-Friendly-Name': 'GroupsCometMembersPageNewMembersSectionRefetchQuery'

    }

    payloads = {

        # cambiare fb_dtsg se cambi account Facebook
        'fb_dtsg': '',
        'fb_api_req_friendly_name': 'GroupsCometMembersPageNewMembersSectionRefetchQuery',
        'variables': f'{variables}',
        'doc_id': ''
        
    }

    try:
        response = requests.post(url, headers=headers, data=payloads)
    
        if response.status_code == 200:
        
            data = response.json()

            lista_users = data['data']['node']['new_members']['edges']
            next_page_flag = data['data']['node']['new_members']['page_info']['has_next_page']
            next_cursor = data['data']['node']['new_members']['page_info']['end_cursor'] 
            
            variables = {"count":10,"id":f"{id_gruppo}","scale":1.5,"cursor":f"{next_cursor}"}
            
            for user in lista_users:
                id = user['node']['id'] 
                FullName = user['node']['name']
                Url = user['node']['url']
                utente = {'id': id, 'FullName': FullName, 'Url': Url}
                utenti.append(utente)

            df = pd.DataFrame(utenti)
            df.to_csv('utenti.csv', index=False)

        else:
            print(f'Errore nella richiesta. Codice di stato: {response.status_code}')

    except Exception as errore:
        print(f"Si è verificato un errore: {errore}")

    time.sleep(2)