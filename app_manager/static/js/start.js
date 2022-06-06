import { redirect, urlWatching, getModule } from "../js/ui/core.js"

async function startRoute(me) {
    debugger;
    await urlWatching($("head base").attr("href"), async (path) => {
        debugger;
        var bodyContainer = $("#body")[0]
        $(bodyContainer).empty();
        if (path[1] == "edit") {
            var view = await me.loadView("app_edit/index.js");
            await view.doEditApp(path[2]);
            await view.render(bodyContainer);
        }
        else if (path[1] == "files") {
           
            var r = await import("./../views/files/files.js");
            var view = await r.default();
            await view.render(bodyContainer);
            await view.init();
        }
        else if (path[1] == "register") {
            var view = await me.loadView("./app_edit/index.js")
            await view.doNewApp(path[2]);
            await view.render(bodyContainer);
        }
        else if (path[1] == "search") {
            var view = await me.loadView("./search/index.js");
            await view.render(bodyContainer);
            view.init()

        }
        else if (window.location.href == $("head base").attr("href")) {
            var view = await me.loadView("./apps/index.js")
            await view.render(bodyContainer);
            await view.init();
        }
    })
}
export { startRoute }