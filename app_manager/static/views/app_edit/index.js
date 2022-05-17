
import { BaseScope, View } from "../sys/BaseScope.js";
import { ui_window } from "../../js/ui/ui_window.js";
import { ui_rect_picker } from "../../js/ui/ui_rect_picker.js";
import { ui_pdf_desk } from "../../js/ui/ui_pdf_desk.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths } from "../../js/ui/core.js"
debugger;
var appEditView = await View(import.meta, class EditAppView extends BaseScope {
    app = {}
    onInit() {
        this.doEditApp(getPaths()[2])
    }
    async doEditApp(appName) {
        this.app = await api.post("apps/app", {
            AppName: appName
        })
        this.$applyAsync();
    }
    async getListOfApps() {
        

    }

});
export default appEditView;