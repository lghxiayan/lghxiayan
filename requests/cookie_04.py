import requests

url = 'https://music.163.com/#/song?id=1901371647'
comment_url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
headers = {
    'referer': 'https://music.163.com/#/song?id=1901371647',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    # 'cookie': 'nts_mail_user=lghxiayan@163.com:-1:1; _iuqxldmzr_=32; _ntes_nuid=7709d1a5ccd886e77651c3aed0f0b344; NMTID=00OXcdUlU6jeDvKV0iZpeg6MxgUu6UAAAF7HrEyhg; WEVNSM=1.0.0; WNMCID=ygcvbz.1628307534539.01.0; WM_TID=xr1khBVAZtdARFAFUAYqz1L9igNaxPij; NTES_P_UTID=DrwNdG6Ez36VXHlRbeoieYcgBfiRmceV|1640132657; NTES_SESS=Ejfbs81LnQjtHgrQi_HoX5nOrSiOBRCKBR1YZ_ec6qC9Ke8zgMqQWiaO.1wUSYGdr5L5HZy_M.qZ.dZ._bOM3hLsjQwN2KSKOOtOMVaG_ugcuzXwaWdOkKvjDLEs94nemp9eRpvjqcvzXpOEML3sseMvoczgjlZaWrt2fsA3NCKNZ2aHcSYnOD0alhdK7JfhNJbsEPFNVQxhC9pBgJSfCHoN7; S_INFO=1640132657|0|3&80##|lghxiayan; P_INFO=lghxiayan@163.com|1640132657|0|mail163|11&26|hub&1640132400&mail163#GR&null#10#0#0|134181&0|mail163&yanxuan_web&imooc|lghxiayan@163.com; MUSIC_EMAIL_U=1b02e232ed644f172064dedb29041f1b90737e9479fc777512a2a4af188b89d977bc45d49b669001f5ccfeeae2da5cfc46b14e3f0c3f8af9d78b6050a17a35e79e297c66b8a8c665; playliststatus=visible; JSESSIONID-WYYY=cvzIVIV0IDqXX2MN4gBpYaa/Av0lh/hmBtIrqruAPjKPYe4l1X257W20k0I4E3Ni2GkpCH10W41RVtzwjdCf+7DW9WbhviqSgWjG4bjrXfcEMPqcGd++7918HtDwR6B5Aiuf0jmIwtXYaHhqfI5rqFSqm9oF24x1+xuDlF/dIPW44z\P:1662087727873; _ntes_nnid=7709d1a5ccd886e77651c3aed0f0b344,1662085927929; WM_NI=vvzjPQ5HRKjtTzr62N/qjF0se39IU9B+rlstp0a3s22rnflvfvGE4m0/pOTaV/SMz8Z3cTHuxWRAyKTioIvslTy3JJputguVWiaFND5ZyTFRstpMSGFmqlnVlIF8XB5MV3g=; WM_NIKE=9ca17ae2e6ffcda170e2e6eebab53386aeabd6d8339a928ea7d45e828a8aacd85994aea4a2e73a8aed86d3f52af0fea7c3b92ab6aab68bd35bf7989eace98098a6bed7b146edafa6a7b379a7edf7aad83382f5be8df280b4f0afd4f23af2aea287ef7ea6aa89a6b767f4f1c0b0d76b96f19daef9349aedadb5cb7fbc899ea2fc4198b7a1aaf579b08cb7d4c942b4abbc88f85e95b7afa7cd50f786b7b5c55ab1acc0aed24d86b3bf8ded5eb0978ad9db4af7939ad4e637e2a3'
}
original_data = {
    'csrf_token': "",
    'cursor': "-1",
    'offset': "0",
    'orderType': "1",
    'pageNo': "1",
    'pageSize': "20",
    'rid': "R_SO_4_1901371647",
    'threadId': "R_SO_4_1901371647"
}

fin_data = {
    'params': 'k22eQ3VF1iEFtbv2flMt1CO3+I14jDgcxVO96J/sO6bJKlcNlUvbetJirGu+7WsOJOcHOOsPsXH1P8jkYPFzhsig0WrTRfYBNlRq+aJnJfK2lNrhd8Xyza9JffpBgabXRCCS4/TqVvKBtXol7tQ5FrxpBtwdV6oqVV6uef9xqF2kxl/+73vdEieDDDoWu9fp7rumbVIdelVmEYd0xH8f4r4rEB0rei5dxnjb3PCccZdDGKBsxyxIJyOuQx1t4BQI23eleUUAC5z4gTjkSVrSl30XRQ7j31ZhBsol1sIrTUE=',
    'encSecKey': '5db55f2111de6c43035f3e17144bf71047da79de918816b4e7d910c5f11bf9033f995f1f166ec44cb4d20fe4b4c9085dc09fe79704678298da05e94cca07595216136e48c8adf5a53fd1fe376eeb1bf418cb52b301340539af4400cad456a3fd37e23500a101d41962c9169c85eff8168d6a8839c34cc5b17386120bab05dd65'
}

# session = requests.session()
resp = requests.post(comment_url, headers=headers)
resp.encoding = 'utf-8'
html = resp.cookies
print(html)
