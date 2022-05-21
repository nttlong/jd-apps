import { } from "../../ui/angular.js"
var rcmpctModule = angular.module("rcmpct-ui", []);
/**
 Được sử dụng lồng vào bên trong các component mà nó cần template
 */
rcmpctModule.directive("rcmpctTemplate", [() => {
    return {
        restrict: "ECA",
        scope: false,
        compile: function (element) {
            var originHtml = element.html();
            element.empty();
            element.remove();
            return {
                pre: function (s, e, a, c, t) {
                    e.parent().attr("data-display-template", encodeURIComponent(escape(originHtml)));
                    e.remove();
                }
            };
        }
    }
}]);

rcmpctModule.directive("rcmpctView", [() => {
    return {
        restrict: "E",
        replace: true,
        template: `<div></div>`,
        link: (s, e, a) => {
            alert(s.url);
            class component {

            }
            a.$observe("resouce", (v) => {
                alert(v);
            });

        }
    }
}]);
rcmpctModule.directive("rcmpctProgressbar", [() => {
    return {
        restrict: "E",
        replace: true,
        template: `<div><div id='progress' style="position:relative;display:none"></div></div>`,
        link: (s, e, a) => {
            
            class component {

            }
            $(e[0]).find("#progress").css({
                "background-color":a.color||"red",
                "left": "0",
                "width": "0%",
                "height":"100%"
            });
            a.$observe("ngValue", v => {
                if (v > 0) {
                    $(e[0]).find("#progress").show();
                    $(e[0]).find("#progress").css({
                        "width": v + "%"
                    });
                }
            });

        }
    }
}]);
export default rcmpctModule 