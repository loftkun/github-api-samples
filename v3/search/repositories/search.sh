#! /bin/bash

set -eu

# Basic Authentication
USER=
PASS=

# also, You can use authenticated requests to getting a higher rate limit.
# See https://developer.github.com/v3/#rate-limiting
TOKEN=

# GitHub search API Endpoint
# See https://developer.github.com/v3/search/
#     https://help.github.com/articles/searching-for-repositories/
API=https://api.github.com/search/repositories

# Search Params
# See https://developer.github.com/v3/search/#parameters
# keywords
# be careful for uri encode (ex. white space -> + )
#KEYWORD="microservice"

# language
LANGUAGE=go

# lower limit of star num
STARS=1000

# sort param
SORT=stars
ORDER=desc

# item num per page
# See https://developer.github.com/v3/#pagination
PER_PAGE=10

# query
QUERY="${KEYWORD}+in:name,description,readme+language:${LANGUAGE}+stars:>=${STARS}&sort=${SORT}&order=${ORDER}&per_page=${PER_PAGE}"

# curl basic authentication param
#CURL_BASIC="-u ${USER}:${PASS}"

# jq query
JQ_QUERY=".items[] | [.full_name , .stargazers_count, .html_url, .description] | @csv"

# starting number of pagenation ( 1-origin )
page=1

while :
do
  #echo "page=${page}"

  # search
  #echo "curl ${CURL_BASIC} \"${API}?q=${QUERY}&page=${page}\""
  #json=$(curl ${CURL_BASIC} "${API}?q=${QUERY}&page=${page}" 2>/dev/null)
  json=$(curl -H "Authorization: token ${TOKEN}" "${API}?q=${QUERY}&page=${page}" 2>/dev/null)

  # check result 
  length=$(echo ${json} | jq -r ".items | length" )
  if [ $length -eq 0 ]; then
    break
  fi

  # echo result
  echo ${json} | jq -r "${JQ_QUERY}"

  ((page++))
done
