var rcpLazyScrollModule = angular.module("rpct-ui", []);
/**
 Được sử dụng lồng vào bên trong các component mà nó cần template
 */
rcpLazyScrollModule.directive("rpctTemplate", [() => {
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
/**
 * How to use: Re-Compact lazy scroll
 * <div rpct-lazy-scroll source='[init data source in scope]' on-request-data=[the function when request more data]>
 * {{dataItem}}
 * </div>
 * 
 * */
rcpLazyScrollModule.directive("rpctLazyScroll", ["$compile",($compile) => {
    return {
        restrict:"A",
        link: (s, e, a) => {
            var itemVar = a.itemVar || "dataItem";
            var __pageSize = a.pageSize||50
            function getParentHeight() {
                return new Promise((resolve, reject) => {
                    function run() {
                        if ($.contains($('body')[0], e[0])) {
                            resolve($(e[0]).parent().innerHeight());
                        }
                        else {
                            setTimeout(run, 10);
                        }
                    }
                    run();
                });
            }

            async function start() {
                var pH = await getParentHeight();
                $(e[0]).parent().css({
                    "max-height": pH
                })
                $(e[0]).css({
                    "max-height": pH,
                    "overflow-y": "auto",
                    "overflow-x":"hidden"
                });
                class component {
                    itemTemplate = "";
                    list = [];
                    scope;
                    pageSize = __pageSize;
                    currentPageIndex = 0;
                    onRequestData = () => { };
                    oldList = [];
                    pItemVar = itemVar
                    constructor(scope) {
                        this.scope = scope;
                    }
                    renderList(renderList, cb) {
                        var me = this;
                        var div = $("<div></div>");
                        var start = this.list.length;
                        var end = start + renderList.length;


                        var index = 0;
                        for (var i = start; i < end; i++) {

                            var n = i / this.pageSize;
                            /*this.currentPageIndex = Math.floor((n) as any);*/

                            var eleItem = $("<div scope-id='{{$parent.$id}}'>" + this.itemTemplate + "</div>");
                            var itemScope = s.$new();
                            itemScope[me.pItemVar] = renderList[index];
                            itemScope["$$index"] = i;
                            itemScope["$$pageIndex"] = this.currentPageIndex;
                            $compile(eleItem)(itemScope);
                            itemScope.$applyAsync();
                            this.list.push(renderList[index]);
                            index++;
                            eleItem.appendTo(div[0]);
                        }
                        var masterScope = this.scope;
                        function watch() {
                            var childrend = div.children(`[scope-id='${masterScope.$id}']`);
                            if ((div.children().length > 0 && childrend.length == div.children().length) || renderList.length == 0) {
                                var ret = $("<div></div>");
                                div.children().each((index, ce) => {
                                    $(ce).contents().appendTo(ret[0]);
                                });
                                cb(ret.contents());
                            }
                            else {
                                setTimeout(watch, 10);
                            }
                        }
                        watch();

                    }
                }
                var cmp = new component(s);
                cmp.itemTemplate = $(e[0]).data().displayTemplate;
                cmp.pageSize = s.$eval(a.pageSize);
                if (cmp.itemTemplate) {
                    cmp.itemTemplate = unescape(decodeURIComponent(cmp.itemTemplate));
                    $(e[0]).removeAttr("data-display-template");
                }
                cmp.list = s.$eval(a.source) || [];
                cmp.renderList(s.$eval(a.source) || [], r => {
                    //$(e[0]).empty();
                    //$(e[0]).scrollTop(0);
                    r.appendTo(e[0]);
                    cmp.oldList = cmp.list;
                });


                s.$watch(a.source, (n, o) => {

                    if (angular.isArray(n)) {
                        if (n !== cmp.oldList) {
                            cmp.renderList(n, r => {
                                $(e[0]).empty();
                                $(e[0]).scrollTop(0);
                                cmp.currentPageIndex = 0;
                                cmp.list = n;
                                r.appendTo(e[0]);
                                cmp.oldList = n;
                            });
                        }
                    }
                });
                $(e[0]).css({
                    "overflow-y": "auto"
                }).on('scroll', function (event) {

                    var y = $(e[0]).scrollTop();
                    var h = $(e[0]).height();
                    var element = event.target;
                    if (element.scrollHeight - element.scrollTop === element.clientHeight) {
                        cmp.onRequestData = s.$eval(a.onRequestData);
                        var function_on_request_data = s[a.onRequestData]
                        if (angular.isDefined(a.onRequestData)) {
                            
                            if (cmp.onRequestData instanceof (async () => { }).constructor) {
                                var evt = document.createEvent('Event');
                                evt.initEvent('lazyLoadOnRquestData', true, true);
                                var old_current_page_index = cmp.currentPageIndex
                                cmp.currentPageIndex = cmp.currentPageIndex + 1;
                                evt["pageIndex"] = cmp.currentPageIndex;
                                evt["pageSize"] = cmp.pageSize;
                                evt["scope"] = s;
                                evt["done"] = (data) => {
                                    if (!data || (data.length == 0))
                                        cmp.currentPageIndex = old_current_page_index;
                                    cmp.renderList(data, r => {
                                        
                                        r.appendTo(e[0]);

                                        
                                    });
                                };
                                cmp.onRequestData(evt).then(r => {
                                    evt["done"](r);
                                });
                            }
                            else if (angular.isFunction(cmp.onRequestData)) {
                                var evt = document.createEvent('Event');
                                evt.initEvent('lazyLoadOnRquestData', true, true);
                                cmp.currentPageIndex = cmp.currentPageIndex + 1;
                                evt["pageIndex"] = cmp.currentPageIndex;
                                evt["pageSize"] = cmp.pageSize;
                                evt["scope"] = s;
                                evt["done"] = (data) => {
                                    cmp.renderList(data, r => {

                                        r.appendTo(e[0]);

                                        console.log(cmp.currentPageIndex);
                                    });
                                };
                                cmp.onRequestData(evt);
                            }
                            else if (cmp.onRequestData && typeof cmp.onRequestData.then === 'function') {

                            }
                            
                        }
                        
                        
                    }
                });
            }

            start().then();
            
        }
    }
}]);
export default rcpLazyScrollModule