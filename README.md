# allkeeper-desktop

<center>
  <img src="https://cdn.icon-icons.com/icons2/2963/PNG/512/macos_big_sur_safe_folder_icon_186055.png"/>
</center>

A desktop version for the project allkeeper(https://github.com/Haoke98/Allkeeper.git)
![](assets/截屏2024-08-02%2017.28.03.png)
![](assets/截屏2024-08-02%2017.08.14.png)
## Build

* It is need to install `libffi`

  The following uses MacOS as an example for demonstration:
  ```shell
  brew install libffi
  ```
  create link:
  ```shell
  sudo ln -s /opt/homebrew/opt/libffi/lib/libffi.8.dylib /usr/local/lib/libffi.8.dylib
  ```
  build:
  ```shell
  python setup.py py2app
  ```

## Develop Plan & TODO

* [ ] 支持lrzsz ( js调起上传下载文件, [pywebview](https://github.com/r0x0r/pywebview)
  支持 [DragDrop](https://pywebview.flowrl.com/examples/drag_drop.html)
  和 [Downloads](https://pywebview.flowrl.com/examples/downloads.html) 对应着 `rz`和 `sz`)
* [ ] 集成SSH客户端
* [ ] 集成各大流行数据库客户端
* [ ] 服务器之间进行双重加密通信
* [ ] Offline mode
    * [ ] change the db to sqlite3
    * [ ] data sync logic

## 引用 & 感谢

* thanks to [r0x0r](https://github.com/r0x0r) for [pywebview](https://github.com/r0x0r/pywebview)
* thanks to [huashengdun](https://github.com/huashengdun) for [webssh](https://github.com/huashengdun/webssh)
* thanks to [billchurch](https://github.com/billchurch) for [webssh2](https://github.com/billchurch/webssh2)
