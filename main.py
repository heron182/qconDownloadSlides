import re
import logging
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
FORMATTER = '%(module)s %(asctime)s %(levelname)s %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO',
                    format=FORMATTER,
                    filename='download.log',
                    filemode='w')
resp = urlopen('http://qconsp.com/schedule/tabular')
soup = BeautifulSoup(resp.read(), 'html.parser')
links = [l.get('href') for l in soup.find_all('a')
         if isinstance(l.get('href'), str) and
         l.get('href').endswith(('ptx', 'pdf'))
         and 'slides' in l.get('href')]
# logger.info(links)
for l in links:
    # download happens here
    match = re.search(r'slides/(.*)', l)
    filename = match.group(1)
    try:
        urlretrieve(l, filename)
        logger.info('Succesfully downloaded %s' % filename)
    except Exception as e:
        logger.error('Error downloading %s' % filename, exc_info=True)
