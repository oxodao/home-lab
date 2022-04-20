import requests
import os

APPS = [ 'gitea', 'jellyfin', 'paperless' ]

os.environ['B2_ACCOUNT_ID'] = 'BACKBLAZE_B2_ACCOUNT_ID'
os.environ['B2_ACCOUNT_KEY'] = 'BACKBLAZE_B2_ACCOUNT_KEY'
os.environ['RESTIC_REPOSITORY'] = 'b2:BUCKET:/restic/'
os.environ['RESTIC_PASSWORD'] = 'RESTIC_PASSWORD'

def alert(msg):
    print(msg)

    requests.post(
        "WEBHOOK_URL",
        json={
            'username': 'Backup Bot',
            'content': msg
        }
    )

alert('-- Starting homelab backup --')

for app in APPS:
    print(f'- Stopping {app}')
    status = os.system(f'cd /opt/docker-apps/{app} && docker-compose down')
    if status != 0:
        alert(f'Error while stopping {app}. Skipping...')
        continue

    status = os.system(f'restic --verbose backup --tag {app} /opt/docker-apps/{app}')
    alert(f'- {app} backed up' if status == 0 else f'Failed to backup {app}')

    print(f'- Starting {app}')
    status = os.system(f'cd /opt/docker-apps/{app} && docker-compose up -d')
    if status != 0:
        print(f'Error while starting {app} again. Skipping...')
