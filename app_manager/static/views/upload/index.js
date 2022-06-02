import { BaseScope, View } from "./../../js/ui/BaseScope.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var uploadFileView = await View(import.meta, class UploadFileView extends BaseScope {
    appName = ""
    info = {}
    setApp(appName) {
        this.appName = appName;
    }
    async doUploadFile() {

        
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
                ChunkSizeInKB: 1024 * 4,
                IsPublic: false
            });
            if (reg.error) {
                msgError(reg.error.message)
                return
            }
            else {
                this.info = reg.data;
                this.$applyAsync();
                var regData = reg.data;
                debugger;
                for (var i = 0; i < regData.NumOfChunks; i++) {
                    var start = i * regData.ChunkSizeInBytes;
                    var end = Math.min((i + 1) * regData.ChunkSizeInBytes, fileUpload.size);
                    var filePartBlog = fileUpload.slice(start, end)
                    var filePart = new File([filePartBlog], fileUpload.name);
                    var chunk = await api.post(`files/${this.appName}/upload/chunk`, {
                        UploadId: regData.UploadId,
                        Index: i,
                        FilePart: filePart
                    });
                    if (chunk.error) {
                        msgError(chunk.error.message)
                        return
                    }
                    this.info = chunk.data;
                    this.$applyAsync();
                }
            }
            
            
        }
        catch (ex) {
            alert(ex);
        }
        
    }
});
export default uploadFileView;