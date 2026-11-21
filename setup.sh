#!/usr/bin/env bash
# Run once per fresh workspace, from the folder that holds make_reel.py
set -e
pip install -q --break-system-packages kokoro-onnx soundfile numpy playwright pillow 2>&1 | tail -1
[ -d icons_pkg ] || (mkdir icons_pkg && cd icons_pkg && npm init -y >/dev/null 2>&1 && npm i lucide-static >/dev/null 2>&1)
mkdir -p models && cd models
[ -f kokoro-v1.0.onnx ] || curl -sL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f voices-v1.0.bin ] || curl -sL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd ..
[ -d skill ] || git clone -q --depth 1 https://github.com/Jakeschincariol/instagram-agent-skill skill
which ffmpeg google-chrome >/dev/null && echo "setup ok"
