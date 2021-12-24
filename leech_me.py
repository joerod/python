import qbittorrentapi
import time
import argparse

parser = argparse.ArgumentParser(
    description='when your torrent is complete its removed from the queue',
    epilog="python leech_me.py --host '192.168.1.221' --password 'Password'"
)
parser.add_argument("--host", required=True, help="IP of machine running qbittorrent")
parser.add_argument("--port", default='8080', help="Port of machine running qbittorrent")
parser.add_argument("--username", default='admin', help="user name to login")
parser.add_argument("--password", required=True, help="password to login")
args = parser.parse_args()

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(host=args.host, port=args.port, username=args.username, password=args.password)

try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

start = time.time()
while(len(qbt_client.torrents_info())>0):
    for torrents in qbt_client.torrents_info():
        print(f'Still leaching: {torrents.name} - {round((torrents.progress * 100),2)}%')
        if(torrents.state in ['uploading','stalledUP']):
            print(f'Removing {torrents.name}')
            qbt_client.torrents_delete(torrent_hashes=torrents.hash)
    time.sleep(60)
else:
  end = time.time()
  print(f'All leached up: {round(end-start, 3)}')
