@echo off
mode con: cols=100 lines=30
title Fake QR Logger Setup
color 0a
cls

py -m pip install -U -r requirements.txt

pause