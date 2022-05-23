
import { BaseScope, View } from "./../../js/ui/BaseScope.js";
//import { ui_window } from "../../js/ui/ui_window.js";
//import { ui_rect_picker } from "../../js/ui/ui_rect_picker.js";
//import { ui_pdf_desk } from "../../js/ui/ui_pdf_desk.js";
import api from "../../js/ClientApi/api.js"
import { redirect, urlWatching, getPaths, msgError } from "../../js/ui/core.js"

var filesView = await View(import.meta, class FilesView extends BaseScope {
    listOfApp = [1]
    currentApp = undefined
    listOfFiles = []
    currentAppName = undefined
    async doStartView() {

        this.listOfApp = await api.post(`apps/admin/list`, {
            Token: window.token
        })
        this.currentApp = this.listOfApp[0];
        this.currentAppName = this.currentApp.Name;
        await this.doLoadAllFiles();
        this.$apply();
    }
    async doLoadAllFileByApp(appName) {
        this.listOfFiles = await api.post(`files/${appName}/list`, {
            Token: window.token
        });
        this.$applyAsync();
    }
    async doLoadAllFiles() {
        var me = this;
        debugger;
        this.listOfFiles = await api.post(`files/${this.currentAppName}/list`, {
            Token: window.token,
            PageIndex: 0,
            PageSize: 20,
            FieldSearch: "FileName",
            ValueSearch: me.fileNameSearchValue
        });
        this.$applyAsync();
    }
    async doSearchByFileName() {
        await this.doLoadAllFiles();
    }
    async doOpenInWindows(item) {
        var r = await import("../player/index.js");
        var player = await r.default();
        player.playByItem(item);
        player.asWindow();



    }
    async doOpenUploadWindow() {
        var uploadForm = await (await import("../upload/index.js")).default();
        uploadForm.setApp(this.currentAppName);
        uploadForm.asWindow();
    }
    async doOpenUploadZipWindow() {
        var uploadZipForm = await (await import("../zip_upload/index.js")).default();
        uploadZipForm.setApp(this.currentAppName);
        uploadZipForm.asWindow();
    }
    doLoadMore(sender) {

        api.post(`files/${sender.scope.currentAppName}/list`, {
            Token: window.token,
            PageIndex: sender.pageIndex,
            PageSize: sender.pageSize,
            FieldSearch: "FileName",
            ValueSearch: sender.scope.fileNameSearchValue
        }).then(r => {
            sender.done(r);
        });

    }
});
export default filesView;