#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
from oauth_test.api import app 
import uvicorn

def main(host="0.0.0.0", port=8080):
    uvicorn.run(app, host=host, port=port)

