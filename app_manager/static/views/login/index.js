import { BaseScope, View } from "./../../js/ui/BaseScope.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var loginView = await View(import.meta, class LoginView extends BaseScope {
    
    async doLogin() {
        debugger;
        var me = this;
        me.data["language"] = me.data["language"]||"vn"
        var ret = await api.post(`accounts/admin/login`, me.data || {});
        if (ret.error) {
            msgError(ret.error.message);
        }
        else {
            if (window.location.href.indexOf("?ret=")> -1) {
                var url = window.location.href.split("?ret=")[1];
                url = decodeURIComponent(url);
                window.location.href = url;
            }
            else {
                var url = ret.data.redirect;
                window.location.href = url;
            }
        }
        console.log(ret);
        this.$apply();
        return ret;
    }
    
});
export default loginView;