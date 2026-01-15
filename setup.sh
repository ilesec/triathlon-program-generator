#!/bin/bash

echo "================================================"
echo "Triathlon Program Generator - Setup Script"
echo "================================================"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"
echo ""

echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

echo "Step 4: Checking for .env file..."
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ""
    echo "================================================"
    echo "IMPORTANT: Configure your API key"
    echo "================================================"
    echo "Please edit the .env file and add your Anthropic API key"
    echo "Then run: python test_setup.py"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
    echo "Running setup test..."
    python test_setup.py
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure your .env file has your ANTHROPIC_API_KEY"
echo "2. Run the web app: python app/main.py"
echo "3. Or try the example: python example.py"
echo ""
