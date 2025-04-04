#!/bin/bash
pip install --user gunicorn
~/.local/bin/gunicorn app:app
