mkdir -p release
hdiutil create -volname "AccessPod+KeyHub" -srcfolder "dist/AccessPod+KeyHub.app" -ov -format UDZO "release/AccessPod+KeyHub.dmg"
