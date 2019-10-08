import requests
import json

# usage
# python3 github.py | jq . -C | less -R

# token
token='your-OAuth-token'

# endpoint
endpoint='https://api.github.com/graphql'

# ratelimit
# https://developer.github.com/v4/query/  ->  rateLimit
# https://developer.github.com/v4/object/ratelimit/
test01={ 'query' : """
  query {
    rateLimit {
      limit
      cost
      remaining
      resetAt
    }
  }
  """
}

# user ( info of currently authenticated user )
# https://developer.github.com/v4/query/  ->  viewer (User!)
# https://developer.github.com/v4/object/user/
test02={ 'query' : """
  query($number_of_repos:Int!) {
    viewer {
      name
      pinnedRepositories(last:$number_of_repos) {
        nodes {
          nameWithOwner
          url
        }
      }
      pullRequests(last:2){
        nodes {
          createdAt
          url
        }
      }
    }
  }
  """
  , 'variables' : { 'number_of_repos' : 3 }
}

# PR and Issue of Repositories
# https://developer.github.com/v4/query/  ->  repository
# https://developer.github.com/v4/object/repository/ -> pullRequests (PullRequestConnection!)
#   https://developer.github.com/v4/object/pullrequestconnection/
# https://developer.github.com/v4/object/repository/ -> issues (IssueConnection!)
#   https://developer.github.com/v4/object/issueconnection/ 
test03={ 'query' : """
  query {
    repository(owner:"python", name:"python-docs-ja") {
      pullRequests(first: 2) {
        nodes {
          title
          url
        }
      }
      issues(last:2, states:CLOSED) {
        edges {
          node {
            title
            url
          }
        }
      }
    }
  }
  """
}
  
# search
# Pythonのスター数ランキングを取得
# https://developer.github.com/v4/query/  ->  search (SearchResultItemConnection!)
# https://developer.github.com/v4/object/searchresultitemconnection/
test04={ 'query' : """
  query {
    search(query: "language:python stars:>=1000 sort:stars", type: REPOSITORY, first: 10) {
      edges {
        node {
          ... on Repository {
            nameWithOwner
            url
            createdAt
            description
            stargazers{
              totalCount
            }
          }
        }
      }
    }
  }
  """
}

def post(query):
    headers = {"Authorization": "bearer " + token}
    res = requests.post(endpoint, json=query, headers=headers)
    if res.status_code != 200:
      raise Exception("failed : {}".format(res.status_code))
    return res.json()

def main():
  tests = [
    test01,
    test02,
    test03,
    test04
  ]
  for i, test in enumerate(tests):
    #print('test{}'.format(i))
    res = post(test)
    print('{}'.format(json.dumps(res)))

if __name__ == '__main__':
  main()
