#!/bin/bash

dockerfile=.github/workflow_files/docker/Dockerfile

if [ "$UPDATE_TAG" = "latest" ] || [ "$UPDATE_TAG" = "nightly" ]
then
  for i in {1..5}
  do
    docker image build --no-cache	 \
      -t aimstack/aimos:$AIM_VERSION -t aimstack/aimos:$UPDATE_TAG --build-arg AIM_VERSION=$AIM_VERSION -f ${dockerfile} . \
      && break || echo "retry attempt ${i}" && sleep 120
  done
else
  for i in {1..5}
  do
    docker image build --no-cache	\
      -t aimstack/aimos:$AIM_VERSION --build-arg AIM_VERSION=$AIM_VERSION -f ${dockerfile} . \
      && break || echo "retry attempt ${i}" && sleep 120
  done
fi
docker image push --all-tags aimstack/aimos
