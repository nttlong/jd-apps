
import { BaseScope, View } from "./sys/BaseScope.js";
import { ui_window } from "../js/ui/ui_window.js";
import { ui_rect_picker } from "../js/ui/ui_rect_picker.js";
import { ui_pdf_desk } from "../js/ui/ui_pdf_desk.js";
import api from "../js/ClientApi/api.js"
var homeView = await View(import.meta, class homeview extends BaseScope {
    list = []
    onInit(){
//        this.loadData("hps-file-test").then();
            this.$applyAsync();
    }
    
    async getListOfApps() {
        this.list = await api.post("apps/list", {});
        this.$applyAsync();
        
    }
    
});
export default homeView;