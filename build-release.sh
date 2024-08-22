mkdir -p release
hdiutil create -volname "AllKeeper" -srcfolder "dist/AllKeeper.app" -ov -format UDZO "release/AllKeeper.dmg"
