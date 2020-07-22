def get_key_length(cipher_text,max_key_length):
    alphabet = sorted(list(set(list(cipher_text))))
    prob = []
    for i in range(2, max_key_length):
        sub = []
        for n in range(i):
            sub.append(calc_ic(cipher_text[n::i], alphabet))
        prob.append((i,sum(sub)/len(sub)))
    #print(prob)
    ic_list = max(prob, key = lambda x: x[1])
    return ic_list[0]
def calc_ic(sub_string, alphabet):
    count = [0 for _ in range(len(alphabet))]
    n = 0
    for i in range(len(sub_string)):
        value = ord(sub_string[i]) - ord(alphabet[0])
        if (value>=0 and value<len(alphabet)):
            count[value] += 1
            n+=1
    ic = sum([x*(x-1) for x in count])/n/(n-1)
    return ic

#cipher_text = 'abcdffffe'
#cipher_text = "vzf>c-COzE/BqDKF8\iHvv\Vrfvil+NVOn|ZCIfDi\iCzv\X8zSA8@RJJA+#zTfQn\MOB_U}COzB_'SUCB`BoIyig'RIzz++wxDyhQ!IvE@VGf'Sn{GEBrU?CyBQi>i'r ZGfXyl\MMG@UToGGC7QRIz7jZuzICl+iDDC<VFfPL5\CBFn,#sfDL_.GTfe)NmfKG8)Cl`'<V8VGNb'zFO70ZDCzP!QGOfnUTvDGBl+L	N7[RuvUGh+l$AUInms_cAJzA|ZtDxiu=CSDp+%8yzQ6\GCzqU+vzf>c-COzE/BqDKF8\iBN7uZAKJQm/zMz7]W8OMyh]JBOv]%?/Fc]iSzC}+oODMhQUBN7\&HfyCm+PWzqBBQCvPf+QlWn,SoBzic]iLIB %8OJib'TFfo`&yzIi4QTBMv+%HfJD_^FFfp='vzMi4]iFvE@:8vNi	%tv7<&KzQClviIz7.ZrI`R_@SCGv{Y8CDQ_{MSF_8RGDNIcQCOOv`VzTfzl?IFfG<V8xDNb+PlvA.BDPwJc]FFy7|YsfOC6.LJLH/BwIfRb+isuG<BqzIRo\W2fR~VBfwC9?PFfG<ZG fRb?SHC]U*CHzim;GMGr.BqMTNn'LBGL{+GfxMo<BlJp-RGDJL4<JZfo`VoFfRb+iDDC<VFfDL_^FFfe'+vfxCh^SST?kZyDKC7/y"
cipher_text = '+vzf>=xsIzP/bqDKF/I8BvG\\vrfvi`vDPOy|zCIfD]I8wzG\\x8zSA/GHDJL+CzTfQ|ICIB\x0cU%COzBUrIOCM`boIyi[rHCzK+KwxDy\\bQCvP@vGf\'S|NwyBCUUCyBQ]E8{\'C zGfXy`ICGG UtoGGC.bHCzijzuzIC`v8xDN<vFfPL,IsvFy,CsfDLUywNfp)nmfKG/tsf`<<v8VGN<rpzOi0zDCzPubwIfyUtvDGB`vB`Ni[ruvUG\\v`f$LUinms\rU*qDzL|ztDxi\x0bDsMDA+E8yzQ-IwwzBUKvzf>=xsIzP/bqDKF/I8vNiuzAKJQ{zpGzi]w8OMy\\JzvOG]E?\n/F=J8MzN}KoODM\\bKvNi\\FHfyC{vFQzBBbQCvP@vGfWy,soBzi=J8FIM E8OJi<rJzfz`FyzIi+bJvMG+EHfJDUKvzfA=GvzMi+J8zvP@P8vNi"pjp\x0ci<FKzQC`{8Czi.zrI`RUGIwGG{y8CDQUNCMF\x0c8rGDNI=bsIOG`vzTfz`FyzfR<v8xDN<vFfvL.bDPwJ=Jvzyi|ysfOC-yBDLS/bwIfR<v8muR<bqzIR}IM\nf#~vBfwC:FFzfR<zG fR<FIBC\rUJCHzi{BwGGC.bqMTN|rBvGW{KGfxM}CrfJA-rGDJL+CzTfz`voFfR<v8xDN<vFfDLUKvzfp\'KvfxC\\KIMT~kzyDKC.zo|'
## should return 6
a = get_key_length(cipher_text,10)
print(a)

