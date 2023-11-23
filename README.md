
# Hiddify Reality Scanner

This scanner will find the best reality sni for you

## Requirement

You need to install our custom xray core in the server using the following command:
```
#remove old xray
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ remove

systemctl stop hiddify-xray

#install hiddify custom xray
bash -c "$(curl -L https://github.com/hiddify/Xray-core-custom/raw/main/install-release.sh)" @ install
```

now you should create a config with empty nameserver in your panel or add the following config 
```
curl -o server_config.json https://raw.githubusercontent.com/hiddify/Hiddify_Reality_Scanner/main/server_config.json

SERVER_IP=$(curl ip.sb)
echo "vless://hiddify@$SERVER_IP:11443/?fp=chrome&security=reality&pbk=Z84J2IelR9ch3k8VtlVhhs5ycBUlXA7wHBWcBrjqnAw&sid=6ba85179e30d4fc2&sni=www.google.com&type=tcp&flow=xtls-rprx-vision&encryption=none#Hiddify"
```

```
xray run -c server_config.json
```
this will create a temporary xray server for you 
you can use the following reality link:

```
vless://hiddify@SERVER_IP:11443/?fp=chrome&security=reality&pbk=Z84J2IelR9ch3k8VtlVhhs5ycBUlXA7wHBWcBrjqnAw&sid=6ba85179e30d4fc2&sni=www.yahoo.com&type=tcp&flow=xtls-rprx-vision&encryption=none#Hiddify
```

## Install it from PyPI

```bash
pip install -U hiddify_reality_scanner
```

## Usage

```bash
python -m hiddify_reality_scanner vless_link
#or
hiddify_reality_scanner vless_link
```
## Advanced Usage
```bash
hiddify_reality_scanner --jobs 10 --sni yahoo.com,google.com vless_link
```


```bash
hiddify_reality_scanner --jobs 10 --sni path_to_domain_file vless_link
```


## results

The results will be stored in results.txt and results.json