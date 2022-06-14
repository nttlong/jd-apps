import { BaseScope, View } from "./../../js/ui/BaseScope.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var loginView = await View(import.meta, class LoginView extends BaseScope {
    
    async doLogin() {
        try {
            var me = this;
            me.data["language"] = me.data["language"] || "vn"
            var ret = await api.formPost(`accounts/token`, {
                username: `${me.data.username}`,
                password: me.data.password
            });
            window.location.href='./'
        }
        catch (e) {
            alert("login fail")
        }
    }
    
});
export default loginView;