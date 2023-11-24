
# Hiddify Reality Scanner

This is a TLS scanner that finds the best Reality SNI for you based on a list of SNIs.

## ⚙️ Installation
The installation of this scanner has 2 parts. The first part is a server-side application and the 2nd part is client-side.


#### 🛠️ Server-side Installation

* First you need to install our custom xray core in the server using the following command:
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
  * `--jobs` defines the number of concurrent scans
  * `--sni` defines the desired SNIs for scanning
 
* If you want to add a list of SNIs, use the following command
```bash
hiddify_reality_scanner --jobs 10 --sni path_to_the_list vless_link
```
* Here:
  * `--jobs` defines the number of concurrent scans
  * `--sni path_to_the_list` desines the path for the list of SNIs

## 📊 Results
The results will be stored in `results.txt` and `results.json`
