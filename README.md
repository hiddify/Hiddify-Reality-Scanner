<base target="_blank">

<div dir="ltr">



[**![Lang_farsi](https://user-images.githubusercontent.com/125398461/234186932-52f1fa82-52c6-417f-8b37-08fe9250a55f.png) &nbsp;فارسی**](README_fa.md)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</div>
<br>
<div align=center markdown="1">
 

![Hiddify Logo](https://user-images.githubusercontent.com/125398461/227777845-a4d0f86b-faa2-4f2b-a410-4aa5f68bfe19.png)

</div>

# Hiddify Reality Scanner

This is a TLS scanner that finds the best Reality SNI for you based on a list of SNIs. For more information about development, you can read through our [Contribution Guidelines](CONTRIBUTING.md) .

## ⚙️ Installation
The installation of this scanner has 2 parts. The first part is a server-side application and the 2nd part is client-side.


#### 🛠️ Server-side Installation

* First you need to install our custom Xray core on the server using the following command:
```
#remove old xray
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ remove

systemctl stop hiddify-xray

#install hiddify custom xray
bash -c "$(curl -L https://github.com/hiddify/Xray-core-custom/raw/main/install-release.sh)" @ install
```

* Now you should create a config with empty nameserver in your panel or add the following config:
```
curl -o server_config.json https://raw.githubusercontent.com/hiddify/Hiddify_Reality_Scanner/main/server_config.json

SERVER_IP=$(curl ip.sb)
echo "vless://hiddify@$SERVER_IP:11443/?fp=chrome&security=reality&pbk=Z84J2IelR9ch3k8VtlVhhs5ycBUlXA7wHBWcBrjqnAw&sid=6ba85179e30d4fc2&sni=www.google.com&type=tcp&flow=xtls-rprx-vision&encryption=none#Hiddify"
```
* Then you need to run the config via Xray like the command below. This will create a temporary Xray server for you :
```
xray run -c server_config.json
```
* You can use your Reality config like the the following link:

```
vless://hiddify@SERVER_IP:11443/?fp=chrome&security=reality&pbk=Z84J2IelR9ch3k8VtlVhhs5ycBUlXA7wHBWcBrjqnAw&sid=6ba85179e30d4fc2&sni=www.yahoo.com&type=tcp&flow=xtls-rprx-vision&encryption=none#Hiddify
```

#### 🛠️ Clinet-side Installation
For client-side, you just need to use Pypi and run the following command:
```bash
pip install -U hiddify_reality_scanner
```

<br>

## 🚀 Basic Usage
In order to run the scanner, use one of the following commands on your client:
```bash
python -m hiddify_reality_scanner vless_link
#or
hiddify_reality_scanner vless_link
```
## 🚀 Advanced Usage
* If you want to consider more items when scanning, use the following command on your client:
```bash
hiddify_reality_scanner --jobs 10 --sni yahoo.com,google.com vless_link
```
* Here:
  * `--jobs` defines the number of concurrent scans.
  * `--sni` defines the desired SNIs for scanning.
 
* If you want to add a list of SNIs, use the following command
```bash
hiddify_reality_scanner --jobs 10 --sni path_to_the_list vless_link
```
* Here:
  * `--jobs` defines the number of concurrent scans.
  * `--sni path_to_the_list` desines the path for the list of SNIs.

## 📊 Results
The results will be stored in `results.txt` and `results.json` on your client. You can use these SNIs as a Reality domain in your server. [How to add relaity domain on Hiddify Manager](https://github.com/hiddify/Hiddify-Manager/wiki/How-to-use-Reality-on-Hiddify)
