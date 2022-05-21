import rcmpctModule from "./directives/rpct/rcmpt.js"
import { } from "./directives/rpct/rcmpact.layout.grid.js"
import { } from "./directives/rpct/lazy_scroll.js";
import { module, module_name } from "./loader/loaderModule.js";
import bs4Module from "./directives/bs4/module.js";
import { } from "./directives/bs4/select.js";
import api from "./ClientApi/api.js"
import { rcmpactModule } from "./directives/rpct/grid.js";
//
//import qNgView from "./directives/ngView.js";
//setServerApiHostUrl("http://192.168.18.36:5010/api/default");

api.setUrl(window.abs_url + "/api")

var appModule = angular.module("app", [module_name,
    rcmpctModule.name,
    bs4Module.name
]);
var appConotroller = appModule.controller("app", ["$scope", function ($scope) {


}]);
export default appModule;