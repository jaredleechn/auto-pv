#coding:utf-8

from bs4 import BeautifulSoup
import urllib2
import random
import time
import json

f = file('./config.json')
config = json.load(f)

def checkProxy(proxy):

  try:

    # ipURL = "http://ip.chinaz.com/"

    publicIpUrl = "http://1111.ip138.com/ic.asp"

    response = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy})).open(publicIpUrl, timeout=5)

    soup = BeautifulSoup(response.read(), "html.parser")

    publicResult = soup.select('center')[0].text

    publicIp = publicResult[publicResult.index('[') + 1 : publicResult.index(']')]

    selfIpUrl = "http://www.ip138.com/ips138.asp?ip=" + publicIp

    response = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy})).open(selfIpUrl)

    soup = BeautifulSoup(response.read(), "html.parser")

    selfResult = soup.select('.ul1 li')[0].text

    print publicResult.encode('utf-8'), '===?', selfResult.encode('utf-8')

    return publicIp

  except:

    print 'checkIp fail for', proxy

    return False

def getRefererList():

  return config['refererList']




def getProxyList(depth = 0):

  if(depth == 0):

    f = open('./proxy.txt', 'r')

    proxyList = f.read().split(',')

    print 'read', len(proxyList), 'proxy from cache'

    return proxyList

  else:

    proxyURL = "http://www.kuaidaili.com/proxylist/"
    # proxyURL = "http://www.kuaidaili.com/free/inha/"

    proxyList = []

    f = open('./proxy.txt', 'w+')

    for x in xrange(1, depth + 1):

      response = urllib2.urlopen(proxyURL + str(x)).read();

      soup = BeautifulSoup(response, "html.parser")

      for line in soup.select('tbody tr'):

        tds = line.select('td')

        if(tds[2].text == u'高匿名'):

          proxyList.append(line.select('td')[0].text + ':' + line.select('td')[1].text)

    f.write(', '.join(proxyList))

    print 'get', len(proxyList), 'proxy from website'

    return proxyList


def getUserAgentList():

  url = "http://whatsmyuseragent.com/CommonUserAgents"

  userAgentList = []

  response = urllib2.urlopen(url).read()

  soup = BeautifulSoup(response, "html.parser")

  for line in soup.select('tbody tr'):

    userAgentList.append(line.select('td')[0].text)

  print 'get', len(userAgentList), 'userAgent form website'

  return userAgentList


def generateHeader(referer, agent):

  headers = {
    # 'Accept-Encoding': 'gzip, deflate',
    # 'X-Forwarded-For': proxyIp.split(':')[0],
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': referer,
    'User-Agent': agent,
    'X-Requested-With': 'XMLHttpRequest'
  }

  return headers



def vote(url, proxy, headers):

  try: 

    request = urllib2.Request(url, headers=headers)

    response = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy})).open(request, timeout=5)

    soup = BeautifulSoup(response.read(), "html.parser")

    score = soup.select('.myinfo .fr .rank em')

    return score[2].string

  except:

    print "error"

    return False


def run(times):

  refererList = getRefererList()

  proxyList = getProxyList(30)

  agentList = getUserAgentList()

  while times > 0:
  
    wait = random.randint(1,10)

    time.sleep(wait)

    url = config['url'] + '&date=' + str(int(time.time() * 1000))
    proxy = random.choice(proxyList)
    headers = generateHeader(random.choice(refererList), random.choice(agentList))

    realIp = checkProxy(proxy)

    if(realIp):

      success = vote(url, proxy, headers)

      if(success):

        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), ":", "view", success, "by", proxy, "after", str(wait) + 's', "with", headers['User-Agent'].split(';')[-1]

        times -= 1


if __name__ == '__main__':
  
  run(1000)


