
import { BaseScope, View } from "../sys/BaseScope.js";
import { ui_window } from "../../js/ui/ui_window.js";
import { ui_rect_picker } from "../../js/ui/ui_rect_picker.js";
import { ui_pdf_desk } from "../../js/ui/ui_pdf_desk.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching } from "../../js/ui/core.js"
debugger;
var appEditView = await View(import.meta, class homeview extends BaseScope {
    list = []
    onInit() {
        
    }
    async doEdit(appName) {
        redirect("edit/" + appName)
    }
    async getListOfApps() {
        

    }

});
export default appEditView;