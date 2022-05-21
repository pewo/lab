#!/bin/sh

ME=$0
DIR=`dirname $ME`
DIR=`dirname $DIR`

if [ ! -d ${DIR}/.git ]; then
	cd ${DIR}/.git
	exit 1
fi

cd ${DIR} 

if [[ ! `git status --porcelain` ]]; then
	echo "Nothing changed"
	exit 0
fi

echo "Adding changes..."
git status

echo "git add ."
git add .

echo git commit -m "Autogit: `date`"
git commit -m "Autogit: `date`"

echo "git push"
git push

