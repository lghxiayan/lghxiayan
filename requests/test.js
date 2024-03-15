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