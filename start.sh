#!/bin/bash
pip install --user gunicorn
~/.local/bin/gunicorn -b 0.0.0.0:$PORT app:app
