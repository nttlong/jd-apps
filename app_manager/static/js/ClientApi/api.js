﻿class api {
    static serverApIHostUrl = ""
    static _onBeforeCall = undefined
    static _onAfterCall = undefined
    static _onError = undefined
    static setUrl(url) {
        this.serverApIHostUrl=url
    }
    static onBeforeCall(callback) {
        api._onBeforeCall = callback;
        return api;
    }
    static onAfterCall(callback) {
        api._onAfterCall = callback;
        return api;
    }
    static onError(callback) {
        api._onError = callback;
        return api;
    }
    static async get(apiPath) {
        var url = this.serverApIHostUrl + "/" + apiPath;
        return await fetch(url)
            .then((response) => {
                return response.json();
            });

    }
    static async post(apiPath, data,noMask) {
        var sender = undefined;
        if (!noMask && api._onBeforeCall) {
            sender = await api._onBeforeCall();
        }
        try {
            var ret = api.__post__(apiPath, data);
            if (!noMask && api._onAfterCall) {
                await api._onAfterCall(sender)
            }
            return ret;
        }
        catch (e) {
            if (!noMask && api._onAfterCall) {
                await api._onAfterCall(sender)
            }
            if (api._onError) {
                await api._onError(e)
            }
        }
    }
    static async __post__(apiPath, data) {
        debugger
        var url = this.serverApIHostUrl + "/" + apiPath;
        function checkHasFile() {
            var retData = {}
            var files = undefined
            var keys = Object.keys(data);
            for (var i = 0; i < keys.length; i++) {
                var val = data[keys[i]];
                if (val instanceof File) {
                    if (!files) files = {}
                    files[keys[i]] = val
                }
                else {
                    retData[keys[i]] = val
                }
            }
            return {
                data: retData,
                files: files
            }
        }
        var checkData = checkHasFile()
        if (!checkData.files) {
           
            var fetcher = await fetch(url, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return await fetcher.json();
        }
        else {
            var formData = new FormData()
            var fileKeys = Object.keys(checkData.files)
            for (var i = 0; i < fileKeys.length; i++) {
                formData.append(fileKeys[i], checkData.files[fileKeys[i]]);
            }
            formData.append('data', JSON.stringify(checkData.data))

            var fetcher = await fetch(url, {
                method: 'POST',
                body: formData
            });
            return await fetcher.json();
        }

    }
}
export default api