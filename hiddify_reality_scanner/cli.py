import traceback
import urllib
import time
import socket
from functools import partial
from httpx_socks import AsyncProxyTransport

import multiprocessing
import argparse

from urllib.parse import urlparse
from jinja2 import Environment, FileSystemLoader
import asyncio
import httpx
import json

import os
import platform
import requests
import zipfile
import shutil
from jinja2 import Environment, PackageLoader, select_autoescape


def get_download_url():
    system = platform.system()
    arch = platform.machine()

    if system == 'Windows':
        return 'https://github.com/hiddify/Xray-core-custom/releases/download/v1.8.6/Xray-windows-64.zip' if arch == 'AMD64' else 'https://github.com/hiddify/Xray-core-custom/releases/download/v1.8.6/Xray-windows-32.zip'
    elif system == 'Darwin': # MacOS
        return 'https://github.com/hiddify/Xray-core-custom/releases/download/v1.8.6/Xray-macos-arm64-v8a.zip' if arch == 'arm64' else 'https://github.com/hiddify/Xray-core-custom/releases/download/v1.8.6/Xray-macos-64.zip'
    elif system == 'Linux':
        return 'https://github.com/hiddify/Xray-core-custom/releases/download/v1.8.6/Xray-linux-64.zip' if arch in ['x86_64', 'AMD64'] else 'https://github.com/hiddify/Xray-core-custom/releases/download/v1.8.6/Xray-linux-32.zip'
    else:
        raise ValueError("Unsupported operating system.")

def download_and_unzip():
    
    download_url = get_download_url()
    extract_to='bin'
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    print(f'downloading xray from {download_url}')
    response = requests.get(download_url, stream=True)
    zip_path = os.path.join(extract_to, 'temp.zip')
    with open(zip_path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    os.remove(zip_path)

def bin_path():
    system = platform.system()
    if system=="Windows":
        return "xray.exe"
    return "xray"

domains_urls=['https://raw.githubusercontent.com/hiddify/Hiddify_Reality_Scanner/main/domains.txt',"https://cdn.jsdelivr.net/gh/hiddify/Hiddify_Reality_Scanner@main/domains.txt"]

def _get_domains_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Split the content of the response into an array of lines
        return response.text.splitlines()
    raise ValueError("no domains  found")

def get_domains(retry=3):
    if retry == 0:
        return ["www.google.com"]
    for url in domains_urls:
        try:
            return _get_domains_from_url(url)    
        except Exception as e:
            print('Error, getting random domains... ', e, 'retrying...', retry)
    
    return get_domains(retry-1)    

def parse_reality(url):
    if not url.startswith("vless://"):
        raise ValueError("only vless reality is accepted")
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)

    # Extract the server_name and server_port from the netloc
    server_name = parsed_url.hostname
    server_port=parsed_url.port

    # Extract other components from the query and fragment
    query_dict = urllib.parse.parse_qs(parsed_url.query)
    short_id = query_dict.get('sid', [''])[0]
    public_key = query_dict.get('pbk', [''])[0]
    uuid = parsed_url.username

    # Create a dictionary with the extracted components
    res= {
        'server_address': server_name,
        'server_port': int(server_port),
        'short_id': short_id,
        'public_key': public_key,
        'uuid': uuid,
        'origsni':query_dict.get('sni', [''])[0],
        'type':query_dict.get('type', ['tcp'])[0],
        'serviceName':query_dict.get('serviceName', [''])[0],
        'mode':query_dict.get('gun', [''])[0],
    }
    if res['type']=='http':
        res['type']='h2'
    return res

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Your CLI Description")

    # Add the command-line arguments
    parser.add_argument("reality_link", help="Vless Reality link")
    parser.add_argument("--jobs",required=False,default=5, type=int,help="Number of concurrent requests (default=4)")
    # parser.add_argument("--server_address", required=False, help="Server address")
    # parser.add_argument("--server_port", required=False, type=int, help="Server port")
    # parser.add_argument("--uuid", required=False, help="UUID")
    # parser.add_argument("--public_key", required=False, help="Public key")
    # parser.add_argument("--short_id", required=False, help="Short ID")
    parser.add_argument("--sni", required=False, help="Domains (comma-separated) or path to file")

    # Parse the command-line arguments
    args = parser.parse_args()

    
    data={}
    if args.reality_link:
        data=parse_reality(args.reality_link)

    # if args.server_address:
    #     data['server_address'] = args.server_address
    # if args.server_port:
    #     data['server_port'] = int(args.server_port)
    # if args.uuid:
    #     data['uuid'] = args.uuid
    # if args.public_key:
    #     data['public_key'] = args.public_key
    # if args.short_id:
    #     data['short_id'] = args.short_id
    
    domains = args.sni.split(',') if args.sni else []  
    if len(domains)==0:
        domains=get_domains()
    if len(domains)==1:
        if os.path.isfile(domains[0]):
            with open(domains[0], 'r') as file:
                domains = file.readlines()
    domains=[d.strip() for d in domains]
    # Now you can use these values in your code
    print(json.dumps(data, indent=4))
    

    bin=bin_path()
    if not os.path.exists(f"bin/{bin}"):
        download_and_unzip()
    
    
    
    # asyncio.run(test_domain(data,domains[0]))
    # asyncio.run(test_domain_async(data,data['origsni']))
    results=run_in_parallel(data,[data['origsni'],*domains],args.jobs)
    print("Finished=============== Sorting results============")
    def custom_sort_key1(item):
        if not item or not item['ping']:
            return 100000000
        return item['ping']
    def custom_sort_key2(item):
        if not item or not item['ping']:
            return -1000000000
        return -item['ping']


    results = sorted(results, key=custom_sort_key2)
    print("\n".join([f"{d['sni']}\t\t:{d['ping']}" for d in results]))
    results = sorted(results, key=custom_sort_key1,)
    with open('results.txt','w') as f:
        f.write("\n".join([f"{d['sni']}\t\t:{d['ping']}" for d in results]))

    with open('results.json','w') as f:
        json.dump(results,f)


def run_in_parallel(data,domains,num_cpu_cores=4):    
    # Create a multiprocessing pool with the desired number of processes
    with multiprocessing.Pool(processes=num_cpu_cores) as pool:
        # Define the fixed parameter that remains the same for all tasks
        
        
        
        
        # Use partial to create a new function with the fixed parameter set
        partial_task = partial(test_domain, data)
        
        # Use the pool to run the tasks in parallel with variable parameters
        results = pool.map(partial_task, domains)
    return results
    
def test_domain(data, domain):
     
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(test_domain_async(data, domain))
    return result

async def test_domain_async(data,d):
    
    try:
        port=find_free_port()
        env = Environment(
            loader=PackageLoader("hiddify_reality_scanner"),
            autoescape=select_autoescape()
        )
        template = env.get_template('xray.json.j2')

        jsondata= template.render(**data,sni=d,port=port)
        # print(jsondata)
        from subprocess import Popen, PIPE
        
        # p = Popen(f'./bin/{bin_path()}',cwd="bin/", stdin=PIPE)
        p = Popen(os.path.abspath(f'./bin/{bin_path()}'),cwd="bin", stdin=PIPE,stdout=PIPE, stderr=PIPE)
        # p.communicate(input=jsondata.encode('utf-8'))    
        p.stdin.write(jsondata.encode('utf-8'))
        p.stdin.close()
        
        await asyncio.sleep(1)
        
        ping_time=await ping("http://cp.cloudflare.com/",port,d)
        print(f"{d}\t\t:{ping_time}")
        
        p.kill()
        return {'ping':ping_time,'sni':d}
    except Exception as e:
        print(f"An error occurred for {d}: {str(e)}")
        
        # Print the stack trace
        traceback.print_exc()
    return {'ping':None,'sni':d}



    
    
    
def find_free_port():
    try:
        # Create a socket with the address family and socket type you need
        # AF_INET for IPv4 and SOCK_STREAM for TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind the socket to a random available port
            s.bind(('localhost', 0))
            
            # Get the port number assigned by the OS
            _, port = s.getsockname()
            
            return port
            # return 9999
    except Exception as e:
        print(f"Error finding a free port: {e}")
        return -1

async def ping(url,port,domain):
    transport = AsyncProxyTransport.from_url(f"socks5://127.0.0.1:{port}")
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            
            start_time = time.time()

            
            response = await client.get(url, timeout=10.0)
            end_time = time.time()
            response.raise_for_status()  # Raise an exception if the request was not successful (e.g., 404, 500)
            
            ping_time = end_time - start_time  # Calculate the ping time
            return int(ping_time*1000)
        except httpx.HTTPError as e:
            # print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f'{domain} {e}')
            return None