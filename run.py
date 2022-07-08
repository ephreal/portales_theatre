#!/bin/python3

import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)

import theatre

application = theatre.application

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True, port=5001)
