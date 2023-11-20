
import requests
import time

birddog_ip_addrs = {'narthex_r': "192.168.2.157", 'narthex_l': "192.168.0.157", 'rear': "192.168.0.157", 'sanctuary_l': "192.168.0.157", 'sanctuary_r': "192.168.0.157"}


def set_ndi_src(ip_addr, ndi_src_str):
    connectTo = {'sourceName': ndi_src_str}
    api_url = "http://"+ip_addr+":8080/connectTo"
    response = requests.post(api_url, json=connectTo)
    return response.status_code

def get_device_info(ip_addr):
    try:
        api_url = "http://"+ip_addr+":8080/about?FirmwareVersion="
        response = requests.get(api_url,timeout=2)
        return response
    except requests.exceptions.ConnectionError:
        print("Connection error occurred")
    return None


def get_active_ndi(ip_addr):
    api_url = "http://"+ip_addr+":8080/List"  # returns active ndi (doesnt refresh)
    response = requests.get(api_url)
    return response.json()

def reset_ndi_list(ip_addr):
    api_url = "http://"+ip_addr+":8080/reset"  # reset NDI sources
    return requests.get(api_url)


if __name__ == '__main__':
    print('Birddog interface script. Looking for active birddogs...\n')
    failures=[]
    for key in birddog_ip_addrs:
        print("Getting status of ")
        print(key, "=", birddog_ip_addrs[key])
        response = get_device_info (birddog_ip_addrs[key])
        if response is None or response.status_code != 200:
            print("Removing ")
            print(key)
            print(" from this session for not responding\n")
            failures.append(key)
            #del birddog_ip_addrs[key]
        else:
            print(response.json())
            print("\n")
    for failed in failures:
        del birddog_ip_addrs[failed]
    res = get_active_ndi(list(birddog_ip_addrs.values())[0]) #just use first one
    print ("Available NDI sources are:")
    print(list(res))
    print("reset NDI source list? y or n?")
    user_input = input('If source is missing please press y to reset NDI source list otherwise press n then enter \n')
    if user_input.lower() in ('y') :
        for key in birddog_ip_addrs:
            reset_ndi_list(birddog_ip_addrs[key])
        print("wait 5 seconds")
        time.sleep(5)
        res = get_active_ndi(list(birddog_ip_addrs.values())[0])  # just use first one
        print("Available NDI sources are:")
        print(list(res))
    ndi_list = list(res)
    i = 0
    for src in ndi_list:
        print(str(i) + " : "+src+"\n")
        i = i + 1
    print("Enter corresponding number then press enter\n")
    user_input = input('Choose NDI source for Narthex \n')
    src = ndi_list[int(user_input)]
    print("setting narthex to " + src)
    if "narthex_l" in birddog_ip_addrs:
        set_ndi_src(birddog_ip_addrs["narthex_l"],src)
    if "narthex_r" in birddog_ip_addrs:
        set_ndi_src(birddog_ip_addrs["narthex_r"],src)
    print ("quit now or keep going to set sanctuary source")
    i = 0
    for src in ndi_list:
        print(str(i) + " : " + src + "\n")
        i = i + 1
    print("Enter corresponding number then press enter\n")
    user_input = input('Choose NDI source for Sanctuary \n')
    src = ndi_list[int(user_input)]
    print("setting sanctuary to " + src)
    if "rear" in birddog_ip_addrs:
        set_ndi_src(birddog_ip_addrs["rear"], src)
    if "sanctuary_l" in birddog_ip_addrs:
        set_ndi_src(birddog_ip_addrs["sanctuary_l"], src)
    if "sanctuary_r" in birddog_ip_addrs:
        set_ndi_src(birddog_ip_addrs["sanctuary_r"], src)
    print("done!")


