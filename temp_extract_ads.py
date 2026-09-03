import os, requests, json
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('META_ACCESS_TOKEN')
account_id = 'act_1872484302849533'
base_url = 'https://graph.facebook.com/v21.0'

params = {
    'access_token': token,
    'fields': 'id,name,adcreatives{body,title,description,call_to_action_type,object_story_spec}',
    'limit': 50,
    'filtering': json.dumps([
        {'field': 'campaign.id', 'operator': 'IN', 'value': [
            '120249471103610456',
            '120248439517370456',
            '120245852805350456',
            '120234245081880456',
            '120224385946500456'
        ]}
    ])
}
r = requests.get(f'{base_url}/{account_id}/ads', params=params)
data = r.json()

output_lines = []

if 'error' in data:
    output_lines.append('ERROR: ' + json.dumps(data['error'], indent=2))
else:
    ads = data.get('data', [])
    output_lines.append(f'Total ads: {len(ads)}\n')
    for ad in ads:
        name = ad.get('name', '?')
        creatives = ad.get('adcreatives', {}).get('data', [])
        for cr in creatives:
            spec = cr.get('object_story_spec', {})
            link_data = spec.get('link_data', {})
            video_data = spec.get('video_data', {})

            has_content = False
            out = [f'=== {name} ===']

            body = cr.get('body', '')
            title = cr.get('title', '')
            desc = cr.get('description', '')
            cta = cr.get('call_to_action_type', '')

            if body:
                out.append(f'  Body: {body[:500]}')
                has_content = True
            if title:
                out.append(f'  Title: {title}')
                has_content = True
            if desc:
                out.append(f'  Desc: {desc}')
            if cta:
                out.append(f'  CTA type: {cta}')

            if link_data:
                ld_msg = link_data.get('message', '')
                ld_name = link_data.get('name', '')
                ld_desc = link_data.get('description', '')
                ld_cta = link_data.get('call_to_action', {}).get('type', '')
                if ld_msg:
                    out.append(f'  [Link] Message: {ld_msg[:500]}')
                    has_content = True
                if ld_name:
                    out.append(f'  [Link] Name/Titular: {ld_name}')
                    has_content = True
                if ld_desc:
                    out.append(f'  [Link] Desc: {ld_desc}')
                if ld_cta:
                    out.append(f'  [Link] CTA: {ld_cta}')

            if video_data:
                vd_msg = video_data.get('message', '')
                vd_title = video_data.get('title', '')
                vd_desc = video_data.get('description', '')
                vd_cta = video_data.get('call_to_action', {}).get('type', '')
                if vd_msg:
                    out.append(f'  [Video] Message: {vd_msg[:500]}')
                    has_content = True
                if vd_title:
                    out.append(f'  [Video] Title/Titular: {vd_title}')
                    has_content = True
                if vd_desc:
                    out.append(f'  [Video] Desc: {vd_desc}')
                if vd_cta:
                    out.append(f'  [Video] CTA: {vd_cta}')

            if has_content:
                output_lines.append('\n'.join(out))
                output_lines.append('')

with open('temp_ads_copy.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print('Archivo guardado: temp_ads_copy.txt')
