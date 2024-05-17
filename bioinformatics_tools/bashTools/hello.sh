#!/usr/local/bin/bash

var="World"

printf "Hello, %s %d\n" "$1" "$2"

echo "Who else is there?"
read name
echo  "Hello, $name!"

echo "What is your favorite thing to do?"
read action
echo "Wow, ${action}ing sounds fun!"
