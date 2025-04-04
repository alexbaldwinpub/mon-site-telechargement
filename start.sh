#!/bin/bash
pip install gunicorn  # Supprimer --user
gunicorn -b 0.0.0.0:$PORT app:app
