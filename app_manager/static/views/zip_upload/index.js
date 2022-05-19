import { BaseScope, View } from "../sys/BaseScope.js";
import { ui_window } from "../../js/ui/ui_window.js";
import { ui_rect_picker } from "../../js/ui/ui_rect_picker.js";
import { ui_pdf_desk } from "../../js/ui/ui_pdf_desk.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var uploadFileView = await View(import.meta, class UploadFileView extends BaseScope {
    appName = ""
    info = {}
    setApp(appName) {
        this.appName = appName;
    }
    async doUploadZipFile() {
        debugger;

        var file = this.$elements.find("#file")[0];
        if (file.files.length == 0) {
            msgError("Please select file");
            return;
        }
        var fileUpload = file.files[0];
        try {
            var reg = await api.post(`files/${this.appName}/zip/upload/register`, {
                FileName: fileUpload.name,
                FileSize: fileUpload.size,
                ChunkSizeInKB: 1024 * 4,
                IsPublic: false
            });

            for (var i = 0; i < reg.NumOfChunks; i++) {
                var start = i * reg.ChunkSizeInBytes;
                var end = Math.min((i + 1) * reg.ChunkSizeInBytes, fileUpload.size);
                var filePartBlog = fileUpload.slice(start, end)
                var filePart = new File([filePartBlog], fileUpload.name);
                var chunk = await api.post(`files/${this.appName}/zip/upload/chunk`, {
                    UploadId: reg._id,
                    Index: i,
                    FilePart: filePart
                });
                this.info = chunk;
                this.$applyAsync();
            }
        }
        catch (ex) {
            alert(ex);
        }

    }
});
export default uploadFileView;