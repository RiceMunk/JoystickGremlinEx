if exist dist\ (
    rm -r -fo dist\.
)

@echo "Building executable ..."
.\venv\Scripts\python.exe -m PyInstaller -y --log-level INFO --clean joystick_gremlin.spec
cd dist
