

class api {
    static serverApIHostUrl=""
    static setUrl(url) {
        this.serverApIHostUrl=url
    }
    static async get(apiPath) {
        var url = this.serverApIHostUrl + "/" + apiPath;
        return await fetch(url)
            .then((response) => {
                return response.json();
            });

    }
    static async post(apiPath, data) {
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