import qbittorrentapi
import time
import argparse
from plexapi.server import PlexServer

parser = argparse.ArgumentParser(
    description='when your torrent is complete its removed from the queue and refresh your Plex library',
    epilog="python leech_me.py --torrent_host '192.168.1.221' --password 'Password' --plex_host '192.168.1.221' --plex_token 'ad8voSaz1f52TjoV4RgK'"
)
parser.add_argument("--torrent_host", required=True, help="IP of machine running qbittorrent")
parser.add_argument("--torrent_port", default='8080', help="Port of machine running qbittorrent")
parser.add_argument("--username", default='admin', help="user name to login")
parser.add_argument("--password", required=True, help="password to login")
parser.add_argument("--plex_host", help="IP of machine running Plex")
parser.add_argument("--plex_port", default='32400', help="IP of machine running Plex")
parser.add_argument("--plex_token", help="token to auth to Plex")
args = parser.parse_args()

# instantiate a qbittorrent client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(host=args.torrent_host, port=args.torrent_port, username=args.username, password=args.password)

try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

if(args.plex_host):
    # instantiate a plex connection 
    try:
        plex = PlexServer("http://" + args.plex_host +  ":" + args.plex_port, args.plex_token)    
    except Exception as e:
        print(e)

start = time.time()
while(len(qbt_client.torrents_info())>0):
    for torrents in qbt_client.torrents_info():
        print(f'Still leaching: {torrents.name} - {round((torrents.progress * 100),2)}%')
        if(torrents.state in ['uploading','stalledUP']):
            print(f'Removing {torrents.name}')
            qbt_client.torrents_delete(torrent_hashes=torrents.hash)
            if(args.plex_host):
                # remove unneeded path info from download
                refresh_path = torrents.save_path.replace('/downloads/','').replace('/','')
                plex.library.section(refresh_path).update()
                print(f'Refreshed Plex path "{refresh_path}"')
                if(len(qbt_client.torrents_info())==0):
                    end = time.time()
                    total_time = round((end-start)/60, 0)
                    plural_time = 'minute' if total_time <= 1 else 'minutes'
                    print(f'All leached up: leaching took {total_time} {plural_time}')
                    quit()
    time.sleep(60)
else:
  end = time.time()
  total_time = round((end-start)/60, 0)
  plural_time = 'minute' if total_time <= 1 else 'minutes'
  print(f'All leached up: leaching took {total_time} {plural_time}')
