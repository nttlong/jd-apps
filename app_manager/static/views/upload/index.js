import { BaseScope, View } from "../sys/BaseScope.js";
import { ui_window } from "../../js/ui/ui_window.js";
import { ui_rect_picker } from "../../js/ui/ui_rect_picker.js";
import { ui_pdf_desk } from "../../js/ui/ui_pdf_desk.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var uploadFileView = await View(import.meta, class UploadFileView extends BaseScope {
    appName=""
    setApp(appName) {
        this.appName = appName;
    }
    async doUploadFile() {
        debugger;
        
        var file = this.$elements.find("#file")[0];
        if (file.files.length == 0) {
            msgError("Please select file");
            return;
        }
        var fileUpload = file.files[0];
        try {
            var reg = await api.post(`files/${this.appName}/upload/register`, {
                FileName: fileUpload.name,
                FileSize: fileUpload.size,
                ChunkSizeInKB: 1024 * 2,
                IsPublic: false
            });
            var chunk = await api.post(`files/${this.appName}/upload/chunk`, {
                UploadId: reg._id,
                Index: 0,
                FilePart: fileUpload
            });
        }
        catch (ex) {
            alert(ex);
        }
        
    }
});
export default uploadFileView;