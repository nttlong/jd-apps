
import { BaseScope, View } from "./sys/BaseScope.js";
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
        await urlWatching($("head base").attr("href"), (path) => {
            $("#home_view").empty();
            if (path[1]=="edit") {
                $('main[role="main"]').hide();
                import("./app_edit/index.js").then(r => {
                    var view = r.default();
                    view.doEditApp(path[2]).then();
                    debugger;
                    view.render($("#home_view")[0]);
                    $("#home_view").show();
                });
                
           }
           if (path[1] == "register") {
               $('main[role="main"]').hide();
               import("./app_edit/index.js").then(r => {
                   var view = r.default();
                   view.doNewApp(path[2]).then();
                   view.render($("#home_view")[0]);
                   $("#home_view").show();
               });

           }
            if (window.location.href == $("head base").attr("href")) {
                $("#home_view").hide();
                $('main[role="main"]').show();
            }
        })
    }
    async doEdit(appName) {
        redirect("edit/" + appName)
    }
    async doNew() {
        redirect("register")
    }
    async getListOfApps() {
        this.list = await api.post("apps/admin/list", {
            Token: window.token
        });
        this.$applyAsync();
        
    }
    
});

export default homeView;