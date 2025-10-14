#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 18:55:29 2025

@author: jack.turton@phe.gov.uk
"""
from fastapi import FastAPI, Request, BackgroundTasks, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

#oauthscheme = OAuth2AuthorizationCodeBearer(
#    authorizationUrl="https://oauth-openshift.apps.ocp-az-uks.ukhsa.gov.uk/oauth/authorize",
#    tokenUrl="https://oauth-openshift.apps.ocp-az-uks.ukhsa.gov.uk/oauth/token",
#)

from typing import Annotated

from authlib.integrations.starlette_client import OAuth

import logging
import sys
log = logging.getLogger('authlib')
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)

service_account_name = 'proxy'

with open('/var/run/secrets/kubernetes.io/serviceaccount/token','r') as fh:
    secret = fh.readlines()[0]

with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace','r') as fh:
    client_id = f'system:serviceaccount:{fh.readlines()[0]}:{service_account_name}'
    
oauth = OAuth()
oauth.register(
    'openshift_internal',
    client_id=client_id,
    client_secret=secret,
    authorize_url="https://oauth-openshift.apps.ocp-az-uks.ukhsa.gov.uk/oauth/authorize",
    access_token_url="https://oauth-openshift.apps.ocp-az-uks.ukhsa.gov.uk/oauth/token",
    #client_kwargs={'scope': 'user:info'}
    scope='user:info'
)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

@app.get("/login/openshift")
async def login_via_openshift(request: Request):
    redirect_uri = request.url_for('auth_via_openshift')
    return await oauth.openshift_internal.authorize_redirect(request, redirect_uri)

@app.get("/auth/openshift")
async def auth_via_openshift(request: Request):
    print(request.url.path,request.headers,request.path_params,request.body)
    #token = await oauth.openshift_internal.fetch_access_token()#method='GET')
    token = await oauth.openshift_internal.authorize_access_token(request)
    user = token['userinfo']
    print(user)
    return dict(user)

@app.post("/token_test")
async def token_test(request: Request):
    print('in token test!!!!!')
    print(request.url.path,request.headers,request.path_params,await request.body())
    return {'userinfo':{'user_name':'test'}}

@app.get("/test")
def auth_test():#token: Annotated[str, Depends(oauthscheme)]):
    """just a test"""
    return {"test": "pass"}#, "token": token}
