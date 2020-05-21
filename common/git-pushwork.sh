#!/bin/bash

git config --global user.email "chelu.g.robert@gmail.com"
git config --global user.name "Robert"
git add --all
git commit -m "$1"
git push origin master

