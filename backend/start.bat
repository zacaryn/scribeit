@echo off
cd %~dp0
echo Starting ScribeIt Backend...
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 