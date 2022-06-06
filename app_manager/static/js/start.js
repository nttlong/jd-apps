import { redirect, urlWatching, getModule } from "../js/ui/core.js"

async function startRoute(me) {
    debugger;
    await urlWatching($("head base").attr("href"), async (path) => {
        debugger;
        var bodyContainer = $("#body")[0]
        var loadPath = "./apps/index.js" //Mặc định lấy trang chủ
        if (path.length > 1) {
            loadPath = "";
            for (var i = 1; i < path.length; i++) {
                loadPath += "/" + path[i]
            }
            loadPath += "/index.js"; // mọi controller nằm trong index.js
            loadPath = "." + loadPath;
        }
        $(bodyContainer).empty();
        var view = await me.loadView(loadPath);
        //await view.doEditApp(path[2]);
        await view.render(bodyContainer);
        await view.init();
        //if (path[1] == "edit") {
        //    var view = await me.loadView("app_edit/index.js");
        //    await view.doEditApp(path[2]);
        //    await view.render(bodyContainer);
        //}
        //else if (path[1] == "files") {
           
        //    var r = await import("./../views/files/files.js");
        //    var view = await r.default();
        //    await view.render(bodyContainer);
        //    await view.init();
        //}
        //else if (path[1] == "register") {
        //    var view = await me.loadView("./app_edit/index.js")
        //    await view.doNewApp(path[2]);
        //    await view.render(bodyContainer);
        //}
        //else if (path[1] == "search") {
        //    var view = await me.loadView("./search/index.js");
        //    await view.render(bodyContainer);
        //    view.init()

        //}
        //else if (window.location.href == $("head base").attr("href")) {
        //    var view = await me.loadView("./apps/index.js")
        //    await view.render(bodyContainer);
        //    await view.init();
        //}
    })
}
export { startRoute }