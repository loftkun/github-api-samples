#! /bin/bash

set -eu

TOKEN=

# Endpoint
API=https://api.github.com/graphql

# user ( info of currently authenticated user )
curl -d @- -X POST -H "Authorization: bearer ${TOKEN}" "${API}" << EOF
  {
    "query": "query { viewer { login }}"
  }
EOF

# response
curl -d @- -X POST -H "Authorization: bearer ${TOKEN}" "${API}" << 'EOF'
  {
    "query": "query($number_of_repos:Int!) {
      viewer {
        name
         repositories(last: $number_of_repos) {
           nodes {
             name
           }
         }
       }
    }",
    "variables": {
      "number_of_repos": 3
    }
  }
EOF

