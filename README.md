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
* [ ] 实现账号体系和APP,网页,小程序...等等之间的多对一的关系
  ```mermaid
  flowchart LR
    P1[王某某] 
    P2[·······]
    P3[张某某]

    AS1{账号体系: 学信网账号体系}
    AS2{············}
    AS3{账号体系: 微信账号体系}
    

    A1(账号1)
    A2(········)
    A3(账号3)
    A4(········)
    A5(账号5)
    A6(········)
    A7(账号2)
    A8(账号4)
    A9(账号6)

    APP1[学信网Web端]
    APP2[研招网Web端]
    APP3[········]
    APP4[········]
    APP5[········]
    APP6[微信]
    APP7[腾讯云]
    APP8[微信开放平台]
    
    
    


    AS1-->APP1
    AS1-->APP2
    AS2-->APP3
    AS3-->APP6
    AS3-->APP7
    AS3-->APP8
    AS2-->APP4
    AS2-->APP5
    
    
    P1--> A1
    P1--> A2
    P1--> A7
    P2--> A3
    P2--> A4
    P2--> A8
    P3--> A5
    P3--> A6
    P3--> A9

    A1-->AS1
    A2-->AS2
    A3-->AS1
    A4-->AS2
    A5-->AS1
    A6-->AS2
    A7-->AS3
    A8-->AS3
    A9-->AS3
  ```

## 引用 & 感谢

* thanks to [r0x0r](https://github.com/r0x0r) for [pywebview](https://github.com/r0x0r/pywebview)
* thanks to [huashengdun](https://github.com/huashengdun) for [webssh](https://github.com/huashengdun/webssh)
* thanks to [billchurch](https://github.com/billchurch) for [webssh2](https://github.com/billchurch/webssh2)
