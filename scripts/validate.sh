#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo " Validating Claude 3.7 Computer Use 2.0 Operator"
echo "=================================================="

python3 -m py_compile claude_computer_operator.py
python3 -m py_compile screen_coordinate_mapper.py

python3 claude_computer_operator.py
python3 screen_coordinate_mapper.py

echo "Validation successful!"
