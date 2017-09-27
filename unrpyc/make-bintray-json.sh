#!/bin/sh
sed -e s/BRANCHNAME/${TRAVIS_BRANCH}/ -e s/VERSION/$(git describe --tags)/ bintray-template.json > bintray.json
