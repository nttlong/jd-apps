import { BaseScope, View } from "./../../js/ui/BaseScope.js";
//import { ui_window } from "../js/ui/ui_window.js";
//import { ui_rect_picker } from "../js/ui/ui_rect_picker.js";
import { ui_pdf_desk } from "./../../js/ui/ui_pdf_desk.js";
import api from "./../../js/ClientApi/api.js"
import { redirect, urlWatching, getModule } from "./../../js/ui/core.js"
/*import appEditView from "./app_edit/index.js"*/
var pdfEditor = await View(import.meta, class PdfEditor extends BaseScope {
    list = []
    async init() {
        debugger;
        var ele = await this.$findEle("#edior");
        console.log(ele);
        new ui_pdf_desk(ele[0])
        
    }
});

export default pdfEditor;