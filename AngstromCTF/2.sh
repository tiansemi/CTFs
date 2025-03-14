#!/usr/bin/env bash

for (( i = 4000; i >= 3500; i-- )); do
	curl https://directory.web.actf.co/$i.html
done
