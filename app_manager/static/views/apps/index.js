import { BaseScope, View } from "./../../js/ui/BaseScope.js";
//import { ui_rect_picker } from "../../js/ui/ui_rect_picker.js";
//import { ui_pdf_desk } from "../../js/ui/ui_pdf_desk.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"
/*import appEditView from "./app_edit/index.js"*/
var appsView = await View(import.meta, class AppsView extends BaseScope {
    list = [{}]
    
    async init() {
        await this.getListOfApps();
    }
    

    //async start() {
    //    var me = this;

    //}
    async doEdit(appName) {
        redirect("edit/" + appName)
    }
    async doNew() {
        redirect("register")
    }
    //async browserAllFiles() {
    //    redirect("files")
    //}
    async getListOfApps() {
        this.list = await api.post("apps/admin/list", {
            Token: window.token
        });
        this.$applyAsync();

    }
    //async loadFullTextSearch() {
    //    redirect("search")
    //}

});

export default appsView;