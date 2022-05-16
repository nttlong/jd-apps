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
}
export default api