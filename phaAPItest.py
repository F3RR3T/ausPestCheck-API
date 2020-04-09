# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 16:43:21 2020

@author: pratt stephen
"""

import http.client, urllib.request, urllib.parse, urllib.error, base64
from uuid import uuid4
import json
from time import ctime
import datetime as dt
from random import randint
import requests as req
#payloadtemplate = dict(bar = 'foo')

# put sub key and partic key in a text file, one key on each line
with open('mykeys.txt', 'r') as keyfile:
  subscriptionKey = keyfile.readline().strip()
  participantKey = keyfile.readline().strip()
####################################
headers = {
  # Request headers
  'participant-key': participantKey,
  'Content-Type': 'application/json',
  'Ocp-Apim-Subscription-Key': subscriptionKey
}

####################################
#def templateUploadPayload(tags):
#  vals = list('abcdef')
#  payload = dict(zip(tags, vals))
#  return payload

####################################
def createPayload(num = 3, state = 'WA', pestID='C', statusProbs = (10, 70,20)):
  payload = []
  pest = getPest(pestID)
  for i in range(num):
    status = randStatus(statusProbs)
    obs = populateObs(state, pest, status)
    payload.append(obs)
  return payload

####################################
def getPest(pestID):
  pest = {
      'T': 'Thaneroclerus buqueti',
      'C': 'Ceratitis capitata',
      'B': 'Bactrocera tryoni',
      'L': 'Lepidosaphes beckii'
      }
  pestID = pestID.upper()
  return (pest.get(pestID) if pest.get(pestID) else 'Ceratitis capitata')
   
####################################
def randStatus(probs):
  st = []
  statuses = ('Present', 'Absent', 'Inconclusive')
  for s, p in zip(statuses, probs):
    st.extend([s] * p)
  myStatus = st[randint(0,99)]
  return myStatus
  
####################################
def populateObs(state, pest, status):
#  progs = {'testProgram'}
  observation = {}
  observation['uid'] = str(uuid4())
  observation['dateOfActivity'] = dt.datetime.now().strftime("%Y-%m-%d")
  observation['entityName'] = pest
  observation['status'] = status       
  observation['latitude'], observation['longitude'] = stateLoc(state)
  observation['programs'] = ('CENT'),
  observation['surveillanceType'] = 'string'
  return observation

####################################
def stateLoc(state):
  """
  Creates a lat/long pair based on the 'state' argument passed in
  by the caller. 
  The 'centre' tuple contains the lat/long and 'width (in whole degrees)'
  of the centre of the 'state' (or the Country 'AUS').
  The return value is not always strictly within the state. 
  """
  try:
    centre = {
      'NSW': (-32, 145, 3),
      'QLD': (-24, 145, 4),
      'VIC': (-36, 144, 2),
      'WA': (-26, 123, 6),
      'SA': (-35, 135, 5),
      'NT': (-21, 133, 5),
      'ACT': (-36, 149, 0),
      'HEARD': (-53, 73, 0),
      'AUS': (-23, 134, 30),
      'TAS': (-42, 146, 1)}[state.upper()]
  #  print('Tuple: ' + state + "  "+ str(centre))
  except KeyError:
    centre = (-23, 134, 3)
    print('Incorrect STATE: ' + state)
  finally:
    lat = randint(centre[0] - centre[2], centre[0] + centre[2])
    lat = str(lat + randint(-5000,5000)/10000)
    long = randint(centre[1] - centre[2], centre[1] + centre[2])
    long = str(long + randint(-5000,5000)/10000)
  return lat, long

####################################
def writeObs(payload):
  lenny = str(len(payload))
  pest = payload[0].get('entityName')
  filename = dt.datetime.now().strftime("%Y%m%d")+'-'+pest+'-'+lenny+'.txt'
  f = open('H:/doc/2020/code/APC-api/' + filename, 'w')
  f.write(str(payload))
  print("wrote " + filename)
  f.close()
  return
####################################
def uploadObs(payload, verbose = False):
   
  params = urllib.parse.urlencode({
  })
  while len(payload):
        
    if verbose: print(payload[0])
    body = json.dumps(payload.pop())
    if verbose: print(body)
    try:
      conn = http.client.HTTPSConnection('apim-apcplus-uat.azure-api.net')
      print('\nConnected')
      conn.request("POST", "/pha-central/api/surveillance-records?%s" % params, body, headers)
      response = conn.getresponse()
  #    print(response)
      data = response.read()
      print(response.status, response.reason)
      if verbose: print(data)
    except Exception as e:
      print("[Errno {0}] {1}".format(e.errno, e.strerror))
      print(type(e), e)
    finally:
      conn.close()

####################################
#headers = setKey()
#tags = ['uid', 'dateOfActivity', 'entityName', 'status', 'latitude', 'longitude']
#payloadtemplate = templateUploadPayload(tags)

#    import time
#ddd = os.path.getmtime(fil)
#time.ctime(ddd)
#import datetime
#datetime.datetime.fromtimestamp(ddd)
#datetime.datetime.fromtimestamp(ddd).strftime("%Y%m%dT%H%M")