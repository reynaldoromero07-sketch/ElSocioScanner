[app]
# (str) Title of your application
title = El Socio Scanner

# (str) Package name
package.name = elsocioscanner

# (str) Package domain (needed for android packaging)
package.domain = org.reynaldo

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
# CRUCIAL: Aquí le decimos que instale Kivy y la librería para el carro
requirements = python3,kivy,obd

# (list) Permissions
# REQUISITO MÁXIMO: Permisos para buscar y conectarse al Bluetooth del carro
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_SCAN, BLUETOOTH_CONNECT, INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Use secure user data directory
android.private_storage = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
