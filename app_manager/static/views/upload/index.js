import { BaseScope, View } from "./../../js/ui/BaseScope.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError, msgOK } from "../../js/ui/core.js"

var uploadFileView = await View(import.meta, class UploadFileView extends BaseScope {
    appName = ""
    info = {}
    data = {}
    setApp(appName) {
        this.appName = appName;
    }
    async doUploadFile() {

        
        var file = this.$elements.find("#file")[0];
        if (file.files.length == 0) {
            msgError(this.$res("Please select file"));
            return;
        }
        var fileUpload = file.files[0];
        try {
            var reg = await api.post(`${this.appName}/files/register`, {
                Data: {
                    FileName: fileUpload.name,
                    FileSize: fileUpload.size,
                    ChunkSizeInKB: 1024 * 3,
                    IsPublic: this.data.IsPublic||false
                }
            });
            if (reg.Error) {
                msgError(reg.Error.Message)
                return
            }
            else {
                this.info = reg.Data;
                this.$applyAsync();
                var regData = reg.Data;
                debugger;
                for (var i = 0; i < regData.NumOfChunks; i++) {
                    var start = i * regData.ChunkSizeInBytes;
                    var end = Math.min((i + 1) * regData.ChunkSizeInBytes, fileUpload.size);
                    var filePartBlog = fileUpload.slice(start, end)
                    var filePart = new File([filePartBlog], fileUpload.name);
                    var chunk = await api.formPost(`${this.appName}/files/upload`, {
                        UploadId: regData.UploadId,
                        Index: i,
                        FilePart: filePart
                    }, true);
                    if (chunk.Error) {
                        msgError(chunk.Error.message)
                        return
                    }
                    this.info = chunk.Data;
                    this.$applyAsync();
                }
                msgOK(this.$res("Upload was conmplete"));
            }
            
            
        }
        catch (ex) {
            alert(ex);
        }
        
    }
});
export default uploadFileView;