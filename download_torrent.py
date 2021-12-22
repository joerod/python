import argparse
import qbittorrentapi

parser = argparse.ArgumentParser(
    description='download your torrent magnets via the command line and qbittorrent',
    epilog="python download_torrent.py --host '192.168.1.221' --password 'Password' --magnet 'magnet:?xt=' --save_location '/downloads/Movies'"
)
parser.add_argument("--host", required=True, help="IP of machine running qbittorrent")
parser.add_argument("--port", default='8080', help="Port of machine running qbittorrent")
parser.add_argument("--username", default='admin', help="user name to login")
parser.add_argument("--password", required=True, help="password to login")
parser.add_argument("--magnet", required=True, help="magnet url")
parser.add_argument("--save_location", required=True, help="where to save the torrent file")
args = parser.parse_args()

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(host=args.host, port=args.port, username=args.username, password=args.password)

try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

qbt_client.torrents_add(urls=args.magnet,save_path=args.save_location)
