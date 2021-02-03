# 系用要求
* 发行版：CentOS Linux release 7.7
* 内核：5.5.9-1.el7.elrepo.x86_64

#### Bind install

```bash
  systemctl stop firewalld && setenforce 0
  systemctl disable firewalld.service
  yum -y install openssl-devel libcap-devel libuv-devel python-pip gcc json-c-devel
  pip install --upgrade pip && pip install ply
  tar xf  bind-9.16.4.tar.xz
  cd bind-9.16.4
  ./configure  --prefix=/usr/local/bind9 --enable-epoll --with-json-c && make -j 15 && make install
  useradd -r -m -d /var/named -s /sbin/nologin named
  mkdir -p /var/log/named && chown -R named.named /var/log/named /usr/local/bind9
  mkdir -p /var/named/data && chown named.named /var/named/data
  echo 'export PATH=$PATH:/usr/local/bind9/sbin' >> /etc/profile
  cd /usr/local/bind9/etc && rndc-confgen > rndc.conf && tail -10 rndc.conf | head -9 | sed s/#\ //g >> named.conf  #生成配置文件
```

#### 开启Bind系统用量信息-json格式信息统计
1、编译时增加 `--with-json-c` 参数、开启Json格式的信息统计 (依赖`json-c-devel`系统包)
2、在named.conf 中新增配置
```bash
statistics-channels {
	inet * port 8080 allow { any; };
};
```
> * 可以替换为具体的监听IP地址
> * any; 可以配置为具体的允许访问本信息统计接口的IP地址
>
3、默认情况下、不按照zone收集统计信息，可以在 zone 配置中通过增加 `zone-statistics yes;`配置启用zone统计
```bash
zone "example.net" in {
     type master; 
     file "master/example.net";
     zone-statistics yes;
};
```
4、访问
* http://serverIP:8080/json
* http://serverIP:8080/json/v1/zone
* http://serverIP:8080/json/v1/traffic
* 等等接口

#### 参考文档
* https://kb.isc.org/docs/aa-01123
* https://downloads.isc.org/isc/bind9/9.16.3/doc/arm/Bv9ARM.ch05.html#statschannels
