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

* [x] 已经实现了与外部 SSH 客户端联动 : [electerm](https://github.com/electerm/electerm.git)
  * [x] 支持lrzsz
* [ ] 实现与Microsoft Remote Desktop联动
  * [ ] 实现用 ms-rd://协议来唤醒
* [ ] 打通与内网穿透工具:Lanproxy 之间的联动
  * [ ] 端口映射配置的同步
  * [ ] 实现基于接口来动态配置端口映射规则
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

    AS1{学信网账号体系}
    AS2{············}
    AS3{微信账号体系}
    

    A1(账号1)
    A2(········)
    A3(账号2)
    A4(········)
    A5(账号3)
    A6(········)
    A7(账号N-2)
    A8(账号N-1)
    A9(账号N)

    APP1[学信网Web端]
    APP2[················]
    APP3[研招网Web端]
    APP4[················]
    APP5[················]
    APP6[················]
    APP7[微信APP]
    APP8[················]
    APP9[腾讯云]
    APP10[················]
    APP11[微信开放平台]

    AS1-->APP1
    AS1-->APP2
    AS1-->APP3
    AS2-->APP4
    AS2-->APP5
    AS2-->APP6
    AS3-->APP7
    AS3-->APP8
    AS3-->APP9
    AS3-->APP10
    AS3-->APP11
    
    P1----> A1
    P1----> A2
    P1----> A7
    P2---> A3
    P2---> A4
    P2---> A8
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
* thanks to [zxdong262](https://github.com/zxdong262) for [electerm](https://github.com/electerm/electerm)
