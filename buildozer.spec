[app]
title = CrackMaster
package.name = crackmaster
package.domain = com.saikonohack
source.dir = .
source.include_exts = py,png,jpg,wav
version = 1.0
requirements = kivy,plyer,babel
android.permissions = INTERNET,VIBRATE,POST_NOTIFICATIONS
android.api = 31
android.minapi = 21
android.sdk = 20
android.ndk = 25b
icon = assets/icon.png
presplash = assets/presplash.png
android.entrypoint = org.kivy.android.PythonActivity

[buildozer]
log_level = 2
warn_on_root = 1