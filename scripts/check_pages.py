import urllib.request

def check():
    for path in ['/','/progress','/question/category']:
        try:
            r=urllib.request.urlopen('http://127.0.0.1:5000'+path, timeout=5)
            data=r.read().decode('utf-8')
            print('===',path,'status',r.getcode())
            print('\n'.join(data.splitlines()[:15]))
        except Exception as e:
            print('ERR',path,e)

if __name__=='__main__':
    check()
