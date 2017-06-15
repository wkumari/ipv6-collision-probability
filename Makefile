# Simple makefile for deploying to App Engine


DIR = $(shell basename `pwd`)

DEFAULT: ;

test:
	dev_appserver.py .

deploy: app.yaml probability.py
	appcfg.py update ../$(DIR)/