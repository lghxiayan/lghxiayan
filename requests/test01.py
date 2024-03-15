import requests
from Crypto.Cipher import AES

from base64 import b64encode
import json

comment_url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
headers = {
    'referer': 'https://music.163.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
# data和data1都是孤勇者，都能正常取值。
data = {
    'params': 'k22eQ3VF1iEFtbv2flMt1CO3+I14jDgcxVO96J/sO6bJKlcNlUvbetJirGu+7WsOJOcHOOsPsXH1P8jkYPFzhsig0WrTRfYBNlRq+aJnJfK2lNrhd8Xyza9JffpBgabXRCCS4/TqVvKBtXol7tQ5FrxpBtwdV6oqVV6uef9xqF2kxl/+73vdEieDDDoWu9fp7rumbVIdelVmEYd0xH8f4r4rEB0rei5dxnjb3PCccZdDGKBsxyxIJyOuQx1t4BQI23eleUUAC5z4gTjkSVrSl30XRQ7j31ZhBsol1sIrTUE=',
    'encSecKey': '5db55f2111de6c43035f3e17144bf71047da79de918816b4e7d910c5f11bf9033f995f1f166ec44cb4d20fe4b4c9085dc09fe79704678298da05e94cca07595216136e48c8adf5a53fd1fe376eeb1bf418cb52b301340539af4400cad456a3fd37e23500a101d41962c9169c85eff8168d6a8839c34cc5b17386120bab05dd65'
}

true_data = {
    'csrf_token': "",
    'cursor': "-1",
    'offset': "0",
    'orderType': "1",
    'pageNo': "1",
    'pageSize': "20",
    'rid': "R_SO_4_1901371647",
    'threadId': "R_SO_4_1901371647"
}

true_data1 = "{\"csrf_token\":\"\"}"

'''
t2x.be3x = function (Y3x, e2x) {
    var i2x = {}
        , e2x = NEJ.X({}, e2x)
        , mo6i = Y3x.indexOf("?");
    if (window.GEnc && /(^|\.com)\/api/.test(Y3x) && !(e2x.headers && e2x.headers[ev4z.BE0x] == ev4z.FB2x) && !e2x.noEnc) {
        if (mo6i != -1) {
            i2x = j2x.he5j(Y3x.substring(mo6i + 1));
            Y3x = Y3x.substring(0, mo6i)
        }
        if (e2x.query) {
            i2x = NEJ.X(i2x, j2x.fO4S(e2x.query) ? j2x.he5j(e2x.query) : e2x.query)
        }
        if (e2x.data) {
            i2x = NEJ.X(i2x, j2x.fO4S(e2x.data) ? j2x.he5j(e2x.data) : e2x.data)
        }
        i2x["csrf_token"] = t2x.gO5T("__csrf");
        Y3x = Y3x.replace("api", "weapi");
        e2x.method = "post";
        delete e2x.query;
        var bKB4F = window.asrsea(JSON.stringify(i2x), buV2x(["流泪", "强"]), buV2x(Rg7Z.md), buV2x(["爱心", "女孩", "惊恐", "大笑"]));
        e2x.data = j2x.cr3x({
            params: bKB4F.encText,
            encSecKey: bKB4F.encSecKey
        })
    }
    var cdnHost = "y.music.163.com";
    var apiHost = "interface.music.163.com";
    if (location.host === cdnHost) {
        Y3x = Y3x.replace(cdnHost, apiHost);
        if (Y3x.match(/^\/(we)?api/)) {
            Y3x = "//" + apiHost + Y3x
        }
        e2x.cookie = true
    }
    chv7o(Y3x, e2x)
}
'''

# JSON.stringify(i2x)
d = true_data1
# buV2x(["流泪", "强"])
e = '010001'
# buV2x(Rg7Z.md)
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
# buV2x(["爱心", "女孩", "惊恐", "大笑"])
g = '0CoJUm6Qyw8W8jud'
# 16位随机字符串，现在把它定死
i = "sAjAP10zUamiebdp"


def get_encSecKey(a, b, c):
    return '1d3b29d2f02fde08061261ee6db9accad9ad7960b15c828ed9b781564c532fac12dab75e2074f680582616923516a92d81f188420123e1e1d40d52f71f13cdb4f66dc7d6d0c184223ed2d19aec520c63360bbf7d2f2f5fc9c8f8085afd12009d902cc4831628b7da35ba5b46ffc5aec7cc1d61c97f39c94a80bc584d4dd9a073'


def enc_params(a, b):
    print(type(a), a)
    print(type(b), b)
    iv = '0102030405060708'
    aes = AES.new(key=b.encode('utf-8'), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)
    bs = aes.encrypt(a)
    print(bs)
    return bs


def get_params(d, e, f, g, i):
    first = enc_params(d, g)
    secend = enc_params(first, i)
    print(secend)
    return secend


# print(json.dumps(true_data))

params = get_params(d, e, f, g, i)
print(params)
encSecKey = get_encSecKey(g, e, f)

# resp = requests.post(comment_url, data=data)
# resp.encoding = 'utf-8'
# html = resp.json()
# # print(html)
# comments = html['data']['comments']
# for i in comments:
#     print(i['user']['nickname'] + " : ", i['content'])
