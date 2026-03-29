#!/bin/bash

# MANDATORY CHECK: Node.js >= 20
NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
if [ "$NODE_VERSION" -lt 20 ]; then
  echo "Error: Node.js version must be 20 or higher. Current version: $(node -v)"
  exit 1
fi
echo "Node.js version check passed: $(node -v)"

# MANDATORY: Mac-optimized setup scripts to prevent EMFILE errors
echo "Installing watchman to prevent file watching errors..."
if ! command -v watchman &> /dev/null; then
    brew install watchman
else
    echo "watchman is already installed."
fi

echo "Increasing file descriptor limit to prevent EMFILE errors..."
ulimit -n 10000

echo "Installing dependencies..."
npm install

echo "Setup complete. You can now run 'npx expo start'."