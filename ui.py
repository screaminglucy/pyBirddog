import tkinter as tk
import tkinter.font as tkFont
import requests
import time
import json

birddog_ip_addrs = {'narthex_r': "192.168.10.100", 'narthex_l': "192.168.0.157", 'rear': "192.168.0.157", 'sanctuary_l': "192.168.0.157", 'sanctuary_r': "192.168.0.157"}


def get_working_ip_addrs ():
    failures = []
    for key in birddog_ip_addrs:
        print("Getting status of ")
        print(key, "=", birddog_ip_addrs[key])
        response = get_device_info (birddog_ip_addrs[key])
        if response is None or response.status_code != 200:
            print("Removing ")
            print(key)
            print(" from this action for not responding\n")
            failures.append(key)
        else:
            print(response.json())
            print("\n")
    birddog_working_ip_addrs = birddog_ip_addrs
    for failed in failures:
        del birddog_working_ip_addrs[failed]
    return birddog_working_ip_addrs

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

class App:
    def __init__(self, root):
        self.txt_ip_sanctuary_rear = tk.StringVar()
        self.txt_ip_sanctuary_r = tk.StringVar()
        self.txt_ip_sanctuary_l = tk.StringVar()
        self.txt_ip_narthex_l = tk.StringVar()
        self.txt_ip_narthex_r = tk.StringVar()
        #setting title
        root.title("BirdDog Config")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        lbl_ip_address_list=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        lbl_ip_address_list["font"] = ft
        lbl_ip_address_list["fg"] = "#333333"
        lbl_ip_address_list["justify"] = "center"
        lbl_ip_address_list["text"] = "IP Addresses"
        lbl_ip_address_list.place(x=40,y=30,width=110,height=30)

        lbl_narthex_l=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        lbl_narthex_l["font"] = ft
        lbl_narthex_l["fg"] = "#333333"
        lbl_narthex_l["justify"] = "center"
        lbl_narthex_l["text"] = "Narthex (left)"
        lbl_narthex_l.place(x=10,y=70,width=91,height=30)

        self.ip_narthex_l=tk.Entry(root,textvariable=self.txt_ip_narthex_l)
        self.ip_narthex_l["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.ip_narthex_l["font"] = ft
        self.ip_narthex_l["fg"] = "#333333"
        self.ip_narthex_l["justify"] = "center"
        self.ip_narthex_l.insert(0, birddog_ip_addrs['narthex_l'])
        self.ip_narthex_l.place(x=100,y=70,width=124,height=30)

        lbl_narthex_r=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        lbl_narthex_r["font"] = ft
        lbl_narthex_r["fg"] = "#333333"
        lbl_narthex_r["justify"] = "center"
        lbl_narthex_r["text"] = "Narthex (right)"
        lbl_narthex_r.place(x=0,y=120,width=103,height=30)

        self.ip_narthex_r=tk.Entry(root,textvariable=self.txt_ip_narthex_r)
        self.ip_narthex_r["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.ip_narthex_r["font"] = ft
        self.ip_narthex_r["fg"] = "#333333"
        self.ip_narthex_r["justify"] = "center"
        self.ip_narthex_r.insert(0, birddog_ip_addrs['narthex_r'])
        self.ip_narthex_r.place(x=100,y=120,width=125,height=30)

        lbl_sanctuary_l=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        lbl_sanctuary_l["font"] = ft
        lbl_sanctuary_l["fg"] = "#333333"
        lbl_sanctuary_l["justify"] = "center"
        lbl_sanctuary_l["text"] = "Sanctuary (left)"
        lbl_sanctuary_l.place(x=0,y=190,width=115,height=30)

        self.ip_sanctuary_l=tk.Entry(root,textvariable=self.txt_ip_sanctuary_l)
        self.ip_sanctuary_l["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.ip_sanctuary_l["font"] = ft
        self.ip_sanctuary_l["fg"] = "#333333"
        self.ip_sanctuary_l["justify"] = "center"
        self.ip_sanctuary_l.insert(0, birddog_ip_addrs['sanctuary_l'])
        self.ip_sanctuary_l.place(x=110,y=190,width=130,height=30)

        lbl_sanctuary_r=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        lbl_sanctuary_r["font"] = ft
        lbl_sanctuary_r["fg"] = "#333333"
        lbl_sanctuary_r["justify"] = "center"
        lbl_sanctuary_r["text"] = "Sanctuary (right)"
        lbl_sanctuary_r.place(x=10,y=240,width=103,height=30)

        self.ip_sanctuary_r=tk.Entry(root,textvariable=self.txt_ip_sanctuary_r)
        self.ip_sanctuary_r["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.ip_sanctuary_r["font"] = ft
        self.ip_sanctuary_r["fg"] = "#333333"
        self.ip_sanctuary_r["justify"] = "center"
        self.ip_sanctuary_r.insert(0, birddog_ip_addrs['sanctuary_r'])
        self.ip_sanctuary_r.place(x=110,y=240,width=131,height=30)

        lbl_sanctuary_rear=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        lbl_sanctuary_rear["font"] = ft
        lbl_sanctuary_rear["fg"] = "#333333"
        lbl_sanctuary_rear["justify"] = "center"
        lbl_sanctuary_rear["text"] = "Sanctuary (rear)"
        lbl_sanctuary_rear.place(x=10,y=290,width=105,height=30)

        self.ip_sanctuary_rear=tk.Entry(root,textvariable=self.txt_ip_sanctuary_rear)
        self.ip_sanctuary_rear["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.ip_sanctuary_rear["font"] = ft
        self.ip_sanctuary_rear["fg"] = "#333333"
        self.ip_sanctuary_rear["justify"] = "center"
        self.ip_sanctuary_rear.insert(0, birddog_ip_addrs['rear'])
        self.ip_sanctuary_rear.place(x=110,y=290,width=133,height=30)

        lbl_ndi_src=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        lbl_ndi_src["font"] = ft
        lbl_ndi_src["fg"] = "#333333"
        lbl_ndi_src["justify"] = "center"
        lbl_ndi_src["text"] = "NDI source"
        lbl_ndi_src.place(x=40,y=390,width=70,height=25)

        self.lst_ndi_src=tk.Listbox(root)
        self.lst_ndi_src["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.lst_ndi_src["font"] = ft
        self.lst_ndi_src["fg"] = "#333333"
        self.lst_ndi_src["justify"] = "center"
        self.lst_ndi_src.insert(0, "None")
        self.lst_ndi_src.place(x=110,y=350,width=313,height=130)

        btn_detect_ndi=tk.Button(root)
        btn_detect_ndi["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        btn_detect_ndi["font"] = ft
        btn_detect_ndi["fg"] = "#000000"
        btn_detect_ndi["justify"] = "center"
        btn_detect_ndi["text"] = "Detect NDI Sources"
        btn_detect_ndi.place(x=440,y=450,width=133,height=30)
        btn_detect_ndi["command"] = self.btn_detect_ndi_command

        btn_set_narthex=tk.Button(root)
        btn_set_narthex["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        btn_set_narthex["font"] = ft
        btn_set_narthex["fg"] = "#000000"
        btn_set_narthex["justify"] = "center"
        btn_set_narthex["text"] = "Set Narthex Source"
        btn_set_narthex.place(x=380,y=100,width=170,height=30)
        btn_set_narthex["command"] = self.btn_set_narthex_command

        btn_set_sanctuary=tk.Button(root)
        btn_set_sanctuary["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        btn_set_sanctuary["font"] = ft
        btn_set_sanctuary["fg"] = "#000000"
        btn_set_sanctuary["justify"] = "center"
        btn_set_sanctuary["text"] = "Set Sanctuary Source"
        btn_set_sanctuary.place(x=380,y=240,width=172,height=30)
        btn_set_sanctuary["command"] = self.btn_set_sanctuary_command

    def btn_detect_ndi_command(self):
        birddog_ip_addrs['sanctuary_l'] = self.txt_ip_sanctuary_l.get()
        birddog_ip_addrs['sanctuary_r'] = self.txt_ip_sanctuary_r.get()
        birddog_ip_addrs['rear'] = self.txt_ip_sanctuary_rear.get()
        birddog_ip_addrs['narthex_r'] = self.txt_ip_narthex_r.get()
        birddog_ip_addrs['narthex_l'] = self.txt_ip_narthex_l.get()
        print(birddog_ip_addrs)
        self.ip_list = get_working_ip_addrs()
        print(self.ip_list)
        for key in self.ip_list:
            reset_ndi_list(self.ip_list[key])
        time.sleep(2)
        res = get_active_ndi(list(self.ip_list.values())[0])  # just use first one
        print("Available NDI sources are:")
        ndi_list = list(res)
        print(ndi_list)
        self.lst_ndi_src.delete(0, tk.END)
        i = 0
        for src in ndi_list:
            self.lst_ndi_src.insert(i, src)
            i = i + 1
        print("detect_ndi")

    def btn_set_narthex_command(self):
        print("set narthex")
        selected_src_index = self.lst_ndi_src.curselection()[0]
        src = self.lst_ndi_src.get(selected_src_index)
        #print(src)
        if "narthex_l" in self.ip_list:
            set_ndi_src(self.ip_list["narthex_l"], src)
        if "narthex_r" in self.ip_list:
            set_ndi_src(self.ip_list["narthex_r"], src)

    def btn_set_sanctuary_command(self):
        print("set sanctuary")
        selected_src_index = self.lst_ndi_src.curselection()[0]
        src = self.lst_ndi_src.get(selected_src_index)
        #print(src)
        if "rear" in self.ip_list:
            set_ndi_src(self.ip_list["rear"], src)
        if "sanctuary_l" in self.ip_list:
            set_ndi_src(self.ip_list["sanctuary_l"], src)
        if "sanctuary_r" in self.ip_list:
            set_ndi_src(self.ip_list["sanctuary_r"], src)

if __name__ == "__main__":
    # Opening JSON file
    f = open('ipcfg.json')

    # returns JSON object as
    # a dictionary
    birddog_ip_addrs = json.load(f)
    f.close()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
