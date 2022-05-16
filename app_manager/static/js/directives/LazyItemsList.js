var mdl = angular.module("ui", []);
var xDirective=mdl.directive("x", [function () {
    return {
        replace: true,
        template:"<div>test</div>"
    }
    
}]);
export default xDirective;