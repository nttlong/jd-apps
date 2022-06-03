import { BaseScope, View } from "./../../js/ui/BaseScope.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var loginView = await View(import.meta, class LoginView extends BaseScope {
    
    async doLogin() {
        debugger;
        var me = this;
        me.data["language"] = me.data["language"]||"vn"
        this.listOfApp = await api.post(`accounts/admin/login`, me.data || {})
        this.$apply();
    }
    
});
export default loginView;