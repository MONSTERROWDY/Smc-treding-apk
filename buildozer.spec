[app]
title = SMC AI Trading
package.name = smctrading
package.domain = org.veer
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
osx.kivy_version = 2.2.1
requirements = hostpython3,python3,kivy==2.2.1,requests,urllib3
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
