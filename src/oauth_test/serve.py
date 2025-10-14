#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
from oauth_test.api import app 
import uvicorn

def main(host="localhost", port=8080):
    uvicorn.run(app, host=host, port=port)

