[app]
title = Cinema Manager
package.name = cinemamanager
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,kivymd,requests,urllib3,chardet,idna
orientation = portrait
osx.kivy_version = 2.0.0
fullscreen = 0

# Android specific configurations
android.accept_sdk_license = True
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk_build_tools_version = 33.0.2
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

