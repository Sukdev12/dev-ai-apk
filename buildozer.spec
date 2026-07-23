[app]
title = Dev AI Agent
package.name = devai
package.domain = org.devai.agent
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 0

# Required Android Permissions
android.permissions = RECORD_AUDIO, INTERNET, FOREGROUND_SERVICE, SYSTEM_ALERT_WINDOW

android.minapi = 21
android.sdk = 33
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
