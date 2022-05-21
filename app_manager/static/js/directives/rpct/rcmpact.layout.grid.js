import rcmpactModule from "./rcmpt.js"
rcmpactModule.directive("rcmpacGrid", [() => {
    return {
        restrict: "E",
        replace: true,
        template: `<div></div>`,
        link: (s, e, a) => {
            alert("OK");
            class component {

            }
            a.$observe("resouce", (v) => {
                alert(v);
            });

        }
    }
}]);


export { rcmpactModule }