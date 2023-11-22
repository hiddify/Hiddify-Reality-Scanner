import traceback
from functools import partial

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
env = Environment(
    loader=PackageLoader("hiddify_reality_scanner"),
    autoescape=select_autoescape()
)

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

def main():  # pragma: no cover
   import argparse

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Your CLI Description")

    # Add the command-line arguments
    parser.add_argument("--server_address", required=True, help="Server address")
    parser.add_argument("--server_port", required=True, type=int, help="Server port")
    parser.add_argument("--uuid", required=True, help="UUID")
    parser.add_argument("--public_key", required=True, help="Public key")
    parser.add_argument("--short_id", required=True, help="Short ID")
    parser.add_argument("--sni", required=False, help="Domains (comma-separated) or path to file")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values of the arguments
    data=dict(
    server_address = args.server_address,
    server_port = args.server_port,
    uuid = args.uuid,
    public_key = args.public_key,
    short_id = args.short_id,
    
    )
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
    
    run_in_parallel(data,domains,1)



def run_in_parallel(data,domains,num_cpu_cores=4):    
    # Create a multiprocessing pool with the desired number of processes
    with multiprocessing.Pool(processes=num_cpu_cores) as pool:
        # Define the fixed parameter that remains the same for all tasks
        
        
        
        
        # Use partial to create a new function with the fixed parameter set
        partial_task = partial(test_domain, data)
        
        # Use the pool to run the tasks in parallel with variable parameters
        results = pool.map(partial_task, domains)
    

async def test_domain(data,d):
    try:
        port=find_free_port()
        template = env.get_template('xray.json')

        jsondata= template.render(*data,sni=d,port=port)
        
        from subprocess import Popen, PIPE
        p = Popen(bin_path(),cwd="bin", stdin=PIPE)
        p.communicate(input=jsondata)    

        await asyncio.sleep(1)
        
        ping_time=await ping("http://cp.cloudflare.com/",port)
        print(f"{d}\t\t:{ping_time}")
        p.kill()
        return {'ping':ping_time,'sni':d}
    except Exception as e:
        print(f"An error occurred for {d}: {str(e)}")
        
        # Print the stack trace
        traceback.print_exc()




    
    
    
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
    except Exception as e:
        print(f"Error finding a free port: {e}")
        return No

async def ping(url,port):
    async with httpx.AsyncClient() as client:
        try:
            start_time = time.time()
            response = await client.get(url,proxies=f"socks5://127.0.0.1:{port}")
            end_time = time.time()
            response.raise_for_status()  # Raise an exception if the request was not successful (e.g., 404, 500)
            ping_time = end_time - start_time  # Calculate the ping time
            return response.text, ping_time
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None, None