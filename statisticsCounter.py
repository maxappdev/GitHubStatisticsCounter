import requests
import numbers

#keys names of user information object
USERNAME_KEY = 'username'
COMMENTS_KEY = 'comments'
LIKES_KEY = 'likes'
DISLIKES_KEY = 'dislikes'

#constants to send URL to API
API_TOKEN = "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"
HEADERS = {'Authorization': 'token %s' % API_TOKEN}
REACTIONS_HEADERS = {'Authorization': 'token %s' % API_TOKEN, 'Accept': 'application/vnd.github.squirrel-girl-preview+json'}

def __createEmptyUserInfo(username : str):
  return {USERNAME_KEY : username, COMMENTS_KEY : 0, LIKES_KEY : 0, DISLIKES_KEY : 0}

def __createEmptyUserInfoIfNotExists(statistics : list, username : str):
  if not __hasUsername(statistics, username):
    statistics.append(__createEmptyUserInfo(username))

def __incrementValue(entry : dict, key : str):
  if isinstance(entry[key], numbers.Number):
    entry[key] = entry[key] + 1
  else:
    print("unable to increment {0} of type {1}".format(key, type(entry[key])))

def __addComment(statistics : list, username : str):
  __createEmptyUserInfoIfNotExists(statistics, username)
  for entry in statistics:
    if entry[USERNAME_KEY] == username:
      __incrementValue(entry, COMMENTS_KEY)
      
def __addLike(statistics : list, username : str):
  __createEmptyUserInfoIfNotExists(statistics, username)
  for entry in statistics:
    if entry[USERNAME_KEY] == username:
      __incrementValue(entry, LIKES_KEY)

def __addDislike(statistics : list, username : str):
  __createEmptyUserInfoIfNotExists(statistics, username)
  for entry in statistics:
    if entry['username'] == username:
      __incrementValue(entry, DISLIKES_KEY)
  
def __hasUsername(statistics : list, username : str):
  result = False
  for entry in statistics:
    if entry['username'] == username:
      result = True
  return result

def countStatistics(link : str):
  linkArr = link.split('/')

  if len(linkArr) < 6:
    print('link is not valid')
    return

  owner = linkArr[3]
  repo = linkArr[4]
  commitShaOrPrNumber = linkArr[6]

  #define if given link is a PR and not a commit 
  isPullRequest = False
  if linkArr[5] == 'pull':
    isPullRequest = True

  baseUrl = "https://api.github.com"
  commitUrl = baseUrl + "/repos/" + owner + "/" + repo + "/commits/" + commitShaOrPrNumber  + "/comments"
  prUrl = baseUrl + "/repos/" + owner + "/" + repo + "/pulls/" + commitShaOrPrNumber  + "/comments"

  URL = commitUrl
  if isPullRequest:
    URL = prUrl

  #getting all comments of commit/PR
  response = requests.get(url = URL, params = {}, headers = HEADERS)
  data = response.json()

  statistics = []

  for comment in data:
    username = comment['user']['login']
    __addComment(statistics, username)

    REACTIONS_URL = baseUrl + "/repos/" + owner + "/" + repo + "/comments/" + str(comment['id'])  + "/reactions"

    if isPullRequest:
      REACTIONS_URL = baseUrl + "/repos/" + owner + "/" + repo + "/pulls/comments/" + str(comment['id'])  + "/reactions"

    #getting all reactions to a specific comment
    response = requests.get(url = REACTIONS_URL, params = {}, headers = REACTIONS_HEADERS)
    reactionsData = response.json()

    for reaction in reactionsData:
      if reaction['content'] == '+1':
        __addLike(statistics, username)
      elif reaction['content'] == '-1':
        __addDislike(statistics, username)

  return statistics
