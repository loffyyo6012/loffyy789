[app]

# (str) Title of your application
title = Network Analyzer

# (str) Package name
package.name = networkanalyzer

# (str) Package domain
package.domain = org.networkanalyzer

# (source.dir) Source code directory
source.dir = .

# (source.include_exts) Include extensions
source.include_exts = py,png,jpg,kv,atlas

# (str) Source code to run
source.main = main.py

# (list) Permissions
android.permissions = INTERNET

# (list) Features
android.features = android.hardware.internet

# (str) Android API level
android.api = 31

# (str) Minimum API level
android.minapi = 21

# (str) Target API level
android.target_api = 31

# (str) Android NDK version
android.ndk = 25b

# (str) Android SDK version
android.sdk = 31

# (bool) Use legacy build tools
android.gradle_dependencies = 

# (str) Log level
log_level = 2

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application will use the internet connection
android.internet = 1

# (list) Application meta-data
android.meta_data = 

# (str) Application icon
# android.icon = data/icon.png

# (str) Application presplash
# android.presplash = data/presplash.png

# (list) Gradle dependencies
p4a.depends = python3,kivy

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (list) The Android archs to build for
android.archs = arm64-v8a,armeabi-v7a

# (bool) Indicate if the application runs in the background
android.background_running = 0

# (str) Requirements
requirements = python3,kivy

# (bool) Presplash is disabled by default
p4a.entrypoint = org.renpy.android.PythonActivity
