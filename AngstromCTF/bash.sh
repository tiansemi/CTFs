#!/usr/bin/env bash

for (( i = 1; i <= 4999; i++ )); do
	curl https://directory.web.actf.co/$i.html
done
