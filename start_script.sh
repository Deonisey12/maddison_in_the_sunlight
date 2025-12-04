#!/bin/bash
source venv/bin/activate
nohup python3 src/__main__.py > output.log 2>&1 &