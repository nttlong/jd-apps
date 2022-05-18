
import { BaseScope, View } from "../sys/BaseScope.js";
import { ui_window } from "../../js/ui/ui_window.js";
import { ui_rect_picker } from "../../js/ui/ui_rect_picker.js";
import { ui_pdf_desk } from "../../js/ui/ui_pdf_desk.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var playerView = await View(import.meta, class PlayerView extends BaseScope {
    data = {}
    async playByItem(item) {
        this.data = item;
        this.$applyAsync();
        
    }
});
export default playerView;