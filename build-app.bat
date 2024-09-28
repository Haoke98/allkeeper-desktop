@echo off
setlocal enabledelayedexpansion
rem 定义要删除的文件夹列表
set folders=dist build .eggs

rem 遍历每个文件夹并删除它们
for %%f in (%folders%) do (
    if exist %%f (
        echo Deleting folder: %%f
        rmdir /q /s "%%f"
    ) else (
        echo Folder %%f does not exist.
    )
)

echo All specified folders have been deleted.
pyinstaller main.spec --distpath=./dist