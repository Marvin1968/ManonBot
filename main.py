import StringIO
import json
import logging
import random
import urllib
import urllib2
import time

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

# date and time stuff
import datetime

TOKEN = '142527518:AAHm8ufqdwHVVH5ktTgStqxBmFFnqM2Jna8'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        try:
        	message = body['message']
        except Exception, e:
        	message = body['edited_message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return
        else:
        	text = text.lower()
        	
        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)
		
        if text.startswith('/'):
            if text == '/start':
                reply('Manon is opgestart!')
                setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Manon is ehh... dicht!')
                setEnabled(chat_id, False)
            elif '/sletmode' in text:
            	reply('Mijn sletmode staat altijd aan, hihi!')
            elif '/kick' in text:
            	reply('Sorry daar doe ik niet aan!')
            elif text == '/jas':
            	time.sleep(random.randrange(10, 59, 2))
            	reply('Hoe zou het met Jas zijn?')
            elif '/zing' in text:
            	reply('Fa waka Manon\r\nCa va bien?\r\nDeze drums drummen alleen voor jou\r\nVoorbeeld voor iedere vrouw\r\nW-O-W, wow!')
            	time.sleep(4)
            	reply('M-A-N-O-N\r\nM-A-N-O-N\r\nM-A-N-O-N (Oeh)\r\nM-A-N-O-N')
            	time.sleep(2)
            	reply('Laat me zingen voor je\n\rManon, kom en transform met Wiwa tron\r\nEn Facetime in je nachtjapon\r\nManon, Manon, Manon\r\nNooit meer dromen van karton\r\nManon, ik heb zin in een wippie op het balkon\r\nManon')
            	time.sleep(4)
            	reply('M-A-N-O-N\r\nM-A-N-O-N\r\nM-A-N-O-N (Oeh)\r\nM-A-N-O-N')
            	time.sleep(2)
            	reply('Manon, ik wil met jou een blokje om\r\nManon, haarkleur kastanje-champignon\r\nManon, ik deel met jou m\'n laatste bonbon\r\nManon, je bent te bon-be-bon-be-bon ton\r\nManon, Manon, ik lees over jou in de colofon\r\nManon, het zit te knallen als een kanon')
            	time.sleep(4)
            	reply('Verliefd op elke letter\r\nVerliefd op elke letter\r\nVerliefd op elke letter\r\nVerliefd op elke letter')
            	time.sleep(2)
            	reply('M-A-N-O-N\r\nM-A-N-O-N\r\nM-A-N-O-N (Oeh)\r\nM-A-N-O-N')
            	time.sleep(2)
            	reply('Je m\'appelle, je m\'appelle\r\nManon, Manon')
            elif '/cls' in text:
            	reply(img=urllib2.urlopen('https://upload.wikimedia.org/wikipedia/commons/4/48/C64_startup_animiert.gif').read())
            	reply(img=urllib2.urlopen('https://fs-uae.net/wp-content/uploads/2012/04/kickstart13.png').read())
            	reply(img=urllib2.urlopen('http://www.guidebookgallery.org/pics/gui/startupshutdown/splash/amigaos204.png').read())
            else:
                reply('Wat zeg je nu?')

        # CUSTOMIZE FROM HERE

        elif 'wie ben jij' in text:
            reply('Ik ben Manon, garderobemeisje in het AmigaCafe: https://amiga.cafe')
        elif (text == 'tijd') or (text == 'tijd!'):
			now = datetime.datetime.now()
			nownl = now + datetime.timedelta(0,7200)
			nownl = nownl.strftime('%H:%M')
			tienen = '13:17'
			elite = '13:37'
			disk = '15:41'
			tape = '15:30'
			elf = '11:11'
			boeing = '07:47'
			negenelf = '09:11'
			negentwaalf = '09:12'
			petro = '12:00'
			negenvierentwintig = '09:24'
			negenvierenveertig = '09:44'
			negenachtentwintig = '09:28'
			negenvierenzestig = '10:04'
			negenveertien = '09:14'
			negendertig = '09:30'
			negenachtenzestig = '10:08'
			negennegenenvijftig = '09:59'
			negenachttien = '09:18'
			negen = '09:00'
			drienulacht = '03:08'
			if nownl == tienen:
				reply('HET. IS. TIJD! \o/')
			elif nownl == elite:
				reply('Vet elitair, deze tijd \o/')
			elif nownl == disk:
				reply('Tik tik tik bwaaaap tik tik tik - het is 15:41! \o/')
			elif nownl == boeing:
				reply(img=urllib2.urlopen('http://www.destentor.nl/polopoly_fs/1.3503834.1353945798!/image/image.jpg_gen/derivatives/landscape_800_600/image-3503834.jpg').read())
			elif nownl == drienulacht:
				reply(img=urllib2.urlopen('http://i.telegraph.co.uk/telegraph/multimedia/archive/01420/magnum_1420289i.jpg').read())
			elif nownl == negenelf:
				gokje = random.randint(0,9)
				if (gokje > 5):
					reply(img=urllib2.urlopen('http://www.activistpost.com/wp-content/uploads/2016/02/twitpic-35.jpg').read())
				else:
					reply(img=urllib2.urlopen('http://ag-spots-2015.o.auroraobjects.eu/2015/04/15/porsche-991-carrera-4-gts-c188215042015123014_1.jpg').read())
			elif nownl == negentwaalf:
				reply(img=urllib2.urlopen('http://cdn.silodrome.com/wp-content/uploads/2015/03/Porsche-912-16.jpg').read())
			elif nownl == negenveertien:
				reply(img=urllib2.urlopen('http://www.bloomberg.com/image/i_8._fsf5CNE.jpg').read())
			elif nownl == negenvierentwintig:
				reply(img=urllib2.urlopen('https://upload.wikimedia.org/wikipedia/commons/0/08/Nationale_oldtimerdag_Zandvoort_2010,_1982_PORSCHE_924,_HD-SB-44.JPG').read())
			elif nownl == negenvierenveertig:
				reply(img=urllib2.urlopen('http://nbache.dk/Maarssen-2005-04/Pic02.jpg').read())
			elif nownl == negenachtentwintig:
				reply(img=urllib2.urlopen('https://upload.wikimedia.org/wikipedia/commons/c/c4/Porsche_928_GTS_hl_blue.jpg').read())
			elif nownl == negenvierenzestig:
				reply(img=urllib2.urlopen('https://upload.wikimedia.org/wikipedia/commons/a/a4/Porsche_964_front_20080515.jpg').read())
			elif nownl == negenachttien:
				reply(img=urllib2.urlopen('https://upload.wikimedia.org/wikipedia/commons/d/dd/2013_Porsche_918_Spyder_(8674620459).jpg').read())
			elif nownl == negendertig:
				reply(img=urllib2.urlopen('http://bestcarmag.com/sites/default/files/3989200porsche-930-04-550ca773d1d81.jpg').read())
			elif nownl == negenachtenzestig:
				reply(img=urllib2.urlopen('http://www.vierenzestig.nl/wp-content/uploads/2013/12/Porsche-968_02.jpg').read())
			elif nownl == negennegenenvijftig:
				reply(img=urllib2.urlopen('https://upload.wikimedia.org/wikipedia/commons/b/bc/Porsche_959_34_rear.jpg').read())
			elif nownl == negen:
				reply(img=urllib2.urlopen('https://upload.wikimedia.org/wikipedia/commons/c/cb/Saab-900-3door.jpg').read())
				reply('Berry?')
			elif nownl == tape:
				reply('Press play on tape! \o/')
			elif nownl == elf:
				reply('STOP- Berry time! http://www.amibay.com/showthread.php?50254-Amiga-4000-desktop&s=4429847aaeea31ab60facba5feef49f9')
			elif nownl == petro:
				reply('De Amiga Technlogies A1200 - mijn favoriete computer en een wereldse prestatie van (vader van Amiga) Petro Tyschtschenko!')
				reply(img=urllib2.urlopen('http://www.amigafuture.de/album_pic.php?pic_id=19384').read())
			else:
				reply('Is het al 13:17 of 13:37? Nee toch? Volgens mij is het ' + nownl + '!')
        elif 'waar is jas' in text:
        	reply('van het leven aan het genieten!')
        elif '1200' in text:
        	reply('De Amiga Technlogies A1200 - mijn favoriete computer en een wereldse prestatie van (vader van Amiga) Petro Tyschtschenko!')
        	reply(img=urllib2.urlopen('http://www.amigafuture.de/album_pic.php?pic_id=19384').read())
        elif 'tmc' in text:
        	reply('...waar komt die zweetlucht ineens vandaan?!')
        elif 'kaas' in text:
        	reply('kaas?! TMC... je ziet hem niet maar je ruikt hem wel!')
        elif 'zweet' in text:
        	reply('Ik ruik iets... iets... zuurs - is TMC in de buurt?!')
        elif 'glen ' in text:
        	reply('die vieze Glen uit Canada? Met die rotte tanden? Bah!')
        elif 'onderbroek' in text:
        	reply('onderbroek!? wie draagt dat tegenwoordig nou nog!')
        elif 'wmdt' in text:
        	reply('WEG. MET. DIE. TROEP. \o/')
        elif 'stinkt' in text:
        	reply('Stinkt? naar vis!?')
        elif 'magic' in text:
        	reply('Magic... die engerd uit Schagen!?')
        elif 'bmw' in text:
        	reply('Dikke BMW! https://www.youtube.com/watch?v=S0vUeJMHoOk')
        elif 'renault' in text:
        	reply('Doe mij maar een Renault Captur!')
        elif 'pompsnol' in text:
        	reply('Pardon?')	
        elif 'ruik' in text:
        	reply('Sniff... sniff... wat ruik ik toch? Is dat vis!?')
        elif 'hoeveel' in text:
        	reply('Jas heeft ongeveer 4x zoveel')
        elif 'dank je manon' in text:
        	reply('Graag gedaan')
        elif 'jeroen tel' in text:
        	reply('Jeroen Tel? Die ken ik wel: muzikant, uitvinder, project manager, researcher, developer, reclame maker, campagnevoerder, en weet ik wat allemaal nog meer!')
        elif '1991' in text:
        	reply('https://www.youtube.com/watch?v=srEjdAjfwdw')
        elif 'courbois' in text:
        	reply(img=urllib2.urlopen('http://cdn.brutsellog.nl/2007/05_MEI/broodje_bal.jpg').read())
        elif 'handtekening' in text:
        	reply(img=urllib2.urlopen('http://i40.tinypic.com/2z8rdqc.jpg').read())
        	reply(img=urllib2.urlopen('http://i1236.photobucket.com/albums/ff443/nikos-rizos/Petro/20121123_012051.jpg').read())
        	reply(img=urllib2.urlopen('http://i1236.photobucket.com/albums/ff443/nikos-rizos/Petro/20121123_011645.jpg').read())
        	reply(img=urllib2.urlopen('http://blog.a-eon.biz/blog/wp-content/uploads/2015/12/Petro_Book.jpg').read())
        	reply(img=urllib2.urlopen('http://i1236.photobucket.com/albums/ff443/nikos-rizos/Petro/20121123_012624.jpg').read())
        elif 'tijd' in text:
        	if 'bus' in text:
        		reply(img=urllib2.urlopen('https://c1.staticflickr.com/4/3593/3452801512_221b986fa2_b.jpg').read())
        	elif 'altijd' not in text:
        		reply(img=urllib2.urlopen('http://vignette1.wikia.nocookie.net/disney/images/c/c9/Tumblr_mvvwp4QVau1qhcrb0o1_1280.jpg/revision/latest?cb=20131108181614').read())
        elif 'jetset' in text:
        	reply('Jetset jumbo!')
        	reply(img=urllib2.urlopen('http://www.sdnl.nl/images/boeing.jpg').read())
        elif 'toyota' in text:
        	reply('Toyota? <evillaugh>ha ha ha</evillaugh>')
        	reply(img=urllib2.urlopen('http://autostrada.tv/wp-content/uploads/2016/06/Le-Mans-2016-Highlights.jpg').read())
        elif 'paul koster' in text:
        	reply(img=urllib2.urlopen('http://agateau.com/2013/01/22/plouf/amos.png').read())
        elif 'saab' in text:
        	reply('Ik hou van Saab!')
        	reply(img=urllib2.urlopen('https://upload.wikimedia.org/wikipedia/commons/e/e5/Saab_900_GLE_(2)_(crop).jpg').read())
        elif 'kuntrus' in text:
        	reply('Er komt anders heel veel moois uit Rusland!!')
        	reply(img=urllib2.urlopen('http://cdn.caughtoffside.com/wp-content/uploads/2014/12/Irina-Shayk-in-stockings.jpg').read())
        elif 'captur' in text:
        	reply('De Renault Captur is mijn favoriete auto!! Zo leuk!!!')
        	reply(img=urllib2.urlopen('http://www.omniauto.it/awpImages/photogallery/2014/19814/photos1280/renault-captur-project-runway_5.jpg').read())
        elif 'kadett' in text:
        	reply('Lekker racen in mijn Opel Kadett!')
        	reply(img=urllib2.urlopen('http://www.autoholic.de/images/resized/galerieOpel-Kadett-E-GSi16V-H4B8.jpg').read())
        elif 'pokemon' in text:
        	reply('Ik speel ook Pokemon Go, kijk maar!')
        	reply(img=urllib2.urlopen('http://blogs-images.forbes.com/insertcoin/files/2016/07/hit-squad.jpg').read())
        elif 'joshua5' in text:
        	reply('Shall we play a game?')

app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
