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

[buildozer]
log_level = 2
warn_on_root = 1

[android]
accept_sdk_license = True
api = 31
minapi = 21
ndk = 25b
archs = arm64-v8a
