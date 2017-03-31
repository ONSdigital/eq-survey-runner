#!/bin/bash

if [ -z "$EQ_DEV_MODE" ]; then
  export EQ_DEV_MODE=True
fi

if [ -z "$EQ_RABBITMQ_ENABLED" ]; then
  export EQ_RABBITMQ_ENABLED=False
fi

if [ -z "$EQ_ENABLE_CACHE" ]; then
  export EQ_ENABLE_CACHE=True
fi

if [ -z "$EQ_MINIMIZE_ASSETS" ]; then
  export EQ_MINIMIZE_ASSETS=False
fi
