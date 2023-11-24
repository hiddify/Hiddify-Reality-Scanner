<base target="_blank">

<div dir="ltr">



[**🇺🇸 English**](README.md)
</div>
<br>
<div align=center markdown="1">
 

![Hiddify Logo](https://user-images.githubusercontent.com/125398461/227777845-a4d0f86b-faa2-4f2b-a410-4aa5f68bfe19.png)

</div>

# اسکنر ریالیتی هیدیفای
این یک اسکنر TLS است که برای شما بهترین SNIهای ریالیتی را بر اساس لیستی از SNIها پیدا می‌کند.

## ⚙️ نصب
نصب این اسکنر دارای دو بخش است. بخش نخست یک اپلیکیشن سمت سرور است که باید روی سرور شما نصب شود و بخش دوم نیز یک اسکریپت سمت کلاینت است که باید روی کامپیوتر شما نصب گردد.


#### 🛠️ نصب سمت سرور
* ابتدا نیاز است شما هسته Xray کاستوم شده ما را روی سرور خود با استفاده از دستور زیر نصب کنید:
<div dir=ltr>
 
```
#remove old xray
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ remove

systemctl stop hiddify-xray

#install hiddify custom xray
bash -c "$(curl -L https://github.com/hiddify/Xray-core-custom/raw/main/install-release.sh)" @ install
```
</div>

* حالا باید یک فایل کانفیگ بت SNI خالی را روی پنل خود ایجاد کنید یا از کانفیگ زیر استفاده نمایید:
<div dir=ltr>
 
```
curl -o server_config.json https://raw.githubusercontent.com/hiddify/Hiddify_Reality_Scanner/main/server_config.json

SERVER_IP=$(curl ip.sb)
echo "vless://hiddify@$SERVER_IP:11443/?fp=chrome&security=reality&pbk=Z84J2IelR9ch3k8VtlVhhs5ycBUlXA7wHBWcBrjqnAw&sid=6ba85179e30d4fc2&sni=www.google.com&type=tcp&flow=xtls-rprx-vision&encryption=none#Hiddify"
```
</div>

* سپس می‌بایست کانفیگ را با Xray مثل کامند زیر اجرا نمایید. این کار یک سرور Xray موقت برای تست ایجاد می‌کند:

<div dir=ltr>
 
```
xray run -c server_config.json
```
</div>
* می‌توانید کانفیگ ریالیتی را به شکل زیر استفاده نمایید.

<div dir=ltr>
 
```
vless://hiddify@SERVER_IP:11443/?fp=chrome&security=reality&pbk=Z84J2IelR9ch3k8VtlVhhs5ycBUlXA7wHBWcBrjqnAw&sid=6ba85179e30d4fc2&sni=www.yahoo.com&type=tcp&flow=xtls-rprx-vision&encryption=none#Hiddify
```
</div>

#### 🛠️ نصب سمت کلاینت
برای سمت کلاینت کافیه از Pypi استفاده نمایید و کامند زیر را ارا نمایید:
<div dir=ltr>
 
```bash
pip install -U hiddify_reality_scanner
```
</div>

<br>

## 🚀 استفاده پایه
جهت اجرای این اسکنر، یکی از دستورات زیر را روی کلاینت خود اجرا نمایید:
<div dir=ltr>
 
```bash
python -m hiddify_reality_scanner vless_link
#or
hiddify_reality_scanner vless_link
```
</div>

## 🚀 استفاده پیشرفته
* اگر بخواهید پارامترهای بیشتری را هنگام اسکن در نظر بگیرید، می‌بایست از دستور زیر روی کلاینت خود استفاده نمایید:
<div dir=ltr>

```bash
hiddify_reality_scanner --jobs 10 --sni yahoo.com,google.com vless_link
```
</div>

* در اینجا:
  * `--jobs` تعداد اسکن همزمان را تعیین می‌کند.
  * `--sni` SNIهای مورد نظر را برای اسکن مشخص می‌کند.
 
* اگر بخواهید لیستی از SNIها را به اسکنر بدهید، می‌بایست از دستور زیر استفاده نمایید:

<div dir=ltr>
 
 ```bash
hiddify_reality_scanner --jobs 10 --sni path_to_the_list vless_link
```
</div>

* در اینجا:
  * `--jobs` تعداد اسکن همزمان را تعیین می‌کند.
  * `--sni path_to_the_list` مسیر مربوط به لیست SNI مورد نظر را مشخص می‌کند.

## 📊 نتایج
خروجی اسکنر در فایل‌های `results.txt` و `results.json`روی کلاینت شما ذخیره می‌گردد. شما می‌توانید از این SNIها برای ایجاد دامنه‌های ریالیتی در سرور خود استفاده نمایید. [نحوه ثبت دامنه ریالیتی در هیدیفای‌منیجر])(https://github.com/hiddify/Hiddify-Manager/wiki/%D8%A2%D9%85%D9%88%D8%B2%D8%B4-%D8%A7%D8%B3%D8%AA%D9%81%D8%A7%D8%AF%D9%87-%D8%A7%D8%B2-Reality-%D8%AF%D8%B1-%D9%87%DB%8C%D8%AF%DB%8C%D9%81%D8%A7%DB%8C)

