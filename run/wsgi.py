#!/bin/usr/env python3

from flask import Flask

from src import electabuzz

electabuzz.run('0.0.0.0', debug=True)