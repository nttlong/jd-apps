
import { BaseScope, View } from "./../js/ui/BaseScope.js";
import { ui_window } from "../js/ui/ui_window.js";
import { ui_rect_picker } from "../js/ui/ui_rect_picker.js";
import { ui_pdf_desk } from "../js/ui/ui_pdf_desk.js";
import api from "../js/ClientApi/api.js"
import { redirect, urlWatching, getModule } from "../js/ui/core.js"
/*import appEditView from "./app_edit/index.js"*/
var homeView = await View(import.meta, class homeview extends BaseScope {
    list = []
    onInit(){
        //        this.loadData("hps-file-test").then();
        
        
    }
    
    async start() {
        var me = this;
        await urlWatching($("head base").attr("href"),async (path) => {
            $("#home_view").empty();
            if (path[1]=="edit") {
                $('#home-page').hide();
                var view= await me.loadView("app_edit/index.js");
                //var view =await import("./app_edit/index.js");
                await view.doEditApp(path[2]);
                await view.render($("#home_view")[0]);
                $("#home_view").show();
                
            }
            if (path[1] == "files") {
                $('#home-page').hide();
                var view = await me.loadView("./files/index.js")
                await view.render($("#home_view")[0]);
                $("#home_view").show();
                await view.doStartView(path[2])
                
                
            }
           if (path[1] == "register") {
               $('#home-page').hide();
               var view = await me.loadView("./app_edit/index.js")
               await  view.doNewApp(path[2]);
               await  view.render($("#home_view")[0]);
               $("#home_view").show();

            }
            if (path[1] == "test") {
                $('#home-page').hide();
                var r = await import("./test/index.js");
                var view = await r.default();
                await view.render($("#home_view")[0]);
                $("#home_view").show();

            }
            if (window.location.href == $("head base").attr("href")) {
                $("#home_view").hide();
                $('#home-page').show();
            }
        })
    }
    async doEdit(appName) {
        redirect("edit/" + appName)
    }
    async doNew() {
        redirect("register")
    }
    async browserAllFiles() {
        redirect("files")
    }
    async getListOfApps() {
        this.list = await api.post("apps/admin/list", {
            Token: window.token
        });
        this.$applyAsync();
        
    }
    
});

export default homeView;