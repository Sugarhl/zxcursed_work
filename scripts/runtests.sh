#!/bin/bash
rm -rf .env
cp .env.test .env && pytest $1