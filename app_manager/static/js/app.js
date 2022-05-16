import { setServerApiHostUrl} from "../views/sys/BaseScope.js"
import xDirective from "./directives/LazyItemsList.js";
import { module, module_name } from "./loader/loaderModule.js";
import api from "./ClientApi/api.js"
//
//import qNgView from "./directives/ngView.js";
//setServerApiHostUrl("http://192.168.18.36:5010/api/default");
debugger;
api.setUrl(window.abs_url+"/api")
var appModule = angular.module("app", [module_name]);
var appConotroller = appModule.controller("app", ["$scope", function ($scope) {


}]);
export default appModule;