﻿if (document.head.getElementsByTagName("base").length == 0) {
    console.error(`
        it looks like thy forget put base tag in head of thy's html page
        see :https://www.w3schools.com/tags/tag_base.asp#:~:text=The%20tag%20specifies%20the,inside%20the%20element.
    `)
}
else if(!document.head.getElementsByTagName("base")[0].href)
{
    console.error(`
        it looks like thy forget put base tag in head of thy's html page
        see; https://www.w3schools.com/tags/tag_base.asp#:~:text=The%20tag%20specifies%20the,inside%20the%20element.
    `)
}
import { ui_window } from "./ui_window.js";
var callbackList = [];
function fecthHtml(url) {
    return new Promise(function (resole, reject) {
        fetch(url).then(function (response) {
            return response.text();
        }).then((html) => {
            resole(html);
        })
            .catch(function (error) {
                reject(error);
            });
    });
}
function newScope(instance) {
    return instance;
}
function getAllKeyOfProtoType(__proto__) {
    var ret = [];
    while (__proto__ != Object.prototype) {
        ret = ret.concat(Object.getOwnPropertyNames(__proto__));
        __proto__ = __proto__.__proto__;
    }
    return ret;
}
function redirect(sub) {
    window.history.pushState({
        id: sub
    }, sub, sub)
}
function getPaths() {
    return window.location.pathname.split('/');
}
var old_time_out = -1
async function urlWatching(base, onchange) {
    if (old_time_out != -1)
        clearTimeout(old_time_out)
    var old_base = "";
    async function  start() {
        if (window.location.href != old_base) {
            if (window.location.pathname.length > 1) {
                await onchange(window.location.pathname.split('/'))
                old_base = window.location.href;
            }
            else {
                await onchange([])
                old_base = window.location.href;
            }
        }
        old_time_out = setTimeout(start,100)
    }
    await start();
}
function getModule(path) {
    return new Promise((r, e) => {
        import(path).then(fx => {
            r(fx)
        }).catch(ex => {
            e(ex)
        })    
    })
    
}
function combine(A, BClass) {
    
    var keys = getAllKeyOfProtoType(A.__proto__).concat(Object.keys(A));
    //keys.forEach(function (k) {
    //    if (!(BClass.prototype[k] && BClass.prototype[k] != null)) {
    //        BClass.prototype[k] = A[k];
           
    //    }
    //});
    BClass.prototype.$scope = A;
    var B = new BClass();
    var keys = getAllKeyOfProtoType(B.__proto__);
    
    keys.forEach(function (k) {
        //if (k[0] != "$" && k!="constructor") {
        //    A.__proto__[k] = B[k];
        //}
        A.__proto__[k] = B[k];
    });
    
    A.__init__(A);
    return A;
}


class BaseView {
    
    i18n_loadFromView() {
        
        window.language="vn";
        var url=`${this.url}.${window.language}.json`;
        
        
        return new Promise((resolve,reject)=>{
            fetch(url)
            .then(response => response.json())
            .then(data => resolve(data))
            .catch(e=>reject(e));;
        })
    }
    i18n_loadFromApp() {
        
        window.language="vn";
        var url=`${document.head.baseURI}static/i18n/${window.language}.json`;
        
        
        return new Promise((resolve,reject)=>{
            fetch(url)
            .then(response => response.json())
            .then(data => resolve(data))
            .catch(e=>reject(e));
        })
    }
    __merege__(a,b){
        var ret ={};
            var keys=Object.keys(a);
            keys.forEach((k,i)=>{
                ret[k.toLowerCase()]=a[k]
            });

            keys=Object.keys(b);
            keys.forEach((k,i)=>{
                ret[k.toLowerCase()]=b[k]
            });
            return ret;
        
    }
    async setUrl(url) {
        var metaInfo = JSON.parse(JSON.stringify(url));
        if (metaInfo.url)
            this.url = metaInfo.url;
        else
            this.url = url;
        
        var items = this.url.split('/');
        var urlLocal = this.url.substring(0, this.url.length - items[items.length - 1].length);
        this.urlLocation = urlLocal;
        this.templateUrl = this.url + ".html";

        var urlId = URL.createObjectURL(new Blob([this.templateUrl]));
        var id = urlId.split('/')[urlId.split('/').length - 1];
        this.id = id;
        var dataPage={}
        var dataApp={}
        try {
            dataPage= await this.i18n_loadFromView(this);
        }
        catch(e){

        }

        try {
            dataApp= await this.i18n_loadFromApp(this);
        }
        catch(e){

        }
        
        this.$i18n=this.__merege__(dataApp,dataPage);
        this.$applyAsync();
        

    }
    $res(key){
        return (this.$i18n||{})[key.toLowerCase()]||key
    }
    async getLayoutHtml() {
        if (!this._layoutHtml)
            this._layoutHtml = await fecthHtml(this.templateUrl);
        return this._layoutHtml;
    }
    getId() {
        return this.id;
    }
    getUrl() {
        return this.url;
    }
    getTemplateUrl() {
        return this.templateUrl;
    }
    onBeforeDestroy(asyncCallBack) {
        this._onBeforeDestroy = asyncCallBack;
    }
    async __render__(ele) {

        var html = await this.getLayoutHtml();
        var compile = angular.element(document.querySelector('[ng-controller]')).injector().get("$compile");
        this.$elements = $("<div class='test'>" + html + "</div>").contents();
        compile(this.$elements)(this);

        this.$elements.appendTo(ele);
        this.$apply();
        
        

    }
    async render(ele) {
        
        var html = await this.getLayoutHtml();
        var compile = angular.element(document.querySelector('[ng-controller]')).injector().get("$compile");
        this.$elements = $("<div class='test'>" + html + "</div>").contents();
        compile(this.$elements)(this);
       
        this.$elements.appendTo(ele);
        this.$apply();
        var me = this;
        function startWatchDestroy() {

            async function run() {
                if (!$.contains($("body")[0], me.$elements[0])) {
                    if (me._onBeforeDestroy) {
                        await me._onBeforeDestroy();
                    }
                    me.$destroy();
                }
                else {
                    setTimeout(await run, 10);
                }
            }
            run();
        }
        startWatchDestroy();
        
    }
    $findEle(selector,timeOut) {
        var me = this;
        timeOut = timeOut || 500;
        var n = timeOut / 100;
        return new Promise((resolve, reject) => {
            function run() {
                if (me.$elements.find(selector).length > 0) {
                    resolve($(me.$elements.find(selector)[0]));
                }
                else {
                    if (n > 0) {
                        setTimeout(run, 100);
                        n--;
                    }
                    else {
                        reject("Timeout,element wasnot found");
                    }
                }
            }
            run();
        });
    }
    async onResize(asyncCallback) {
        this._onResize = asyncCallback;
        return this;
    }
    async asWindow() {
        var win = new ui_window();
        var tmpDir = $("<div></div>");
        await this.__render__(tmpDir[0]);
        win.setBody(tmpDir[0]);
        await win.show();
        var me = this;
        await win.onBeforeClose(async function () {
            var ret = true;
            if (me._onBeforeDestroy) {
               ret= await me._onBeforeDestroy();
            }
            return ret;
        });
        await win.onAfterClose(async function () {
            tmpDir.remove();
            me.$destroy();
        });
        await win.onResize(async (x,y) => {
            if (me._onResize) {
                await me._onResize(x, y);
                me.$elements.css({
                    "min-width": x,
                    "min-height": y
                })
            }
        });
    }
    async loadView(relUrl) {
        if (relUrl.substring(0, 2) == "./") {
            relUrl = relUrl.substring(2, relUrl.length);
        }

        var urlOfView = this.urlLocation + relUrl;
        var r = await import(urlOfView);
        var view = await r.default();
        return view;
    }
    onInit() {
        console.log(this.__proto__.constructor.name + " has init");
    }
    __init__(scope) {
        var me = this;
        var keys = Object.getOwnPropertyNames(this.__proto__);
        keys.forEach(function (v) {
            scope.__proto__[v] = me.__proto__[v];
        });
        if (this.onInit) {
            var fn = this.onInit();
            if (fn instanceof (Promise)) {
                fn.then().catch(function (err) {
                    console.error(err);
                });
            }
        }
    }
}
function View(url, classView) {
     async function applyResolve(scope) {
        scope = scope || angular.element(document.body).scope().$root;

         var subScope = scope.$new(true);
         
        subScope = combine(subScope, classView)
        await subScope.setUrl(url);
        return subScope;
    };
    return new Promise(function (resolve, reject) {
        function watcher(cb) {
            function run() {
                if (angular.element(document.body).scope()) {
                    cb(angular.element(document.body).scope())
                }
                else {
                    setTimeout(run, 10);
                }
            };
            run();
        };
        new watcher(function () {
            
            resolve(applyResolve);
        });

    });

}
function postId(view, id, callback) {
    function run(view, handlerId, cb) {
        function w(view, handlerId, cb) {
            var count = $(`script[ui-id='${handlerId}']`).length;
            if (count == 0) {
                setTimeout(function () {
                    w(view, handlerId, cb)
                }, 10);
            }
            else {
                
                cb()
            }
        }
        w(view, handlerId, cb)
    }
    new run(view, id, function () {
        callback();
    });
}
function msgError(msg) {
    $.toast({
        text: msg,
        showHideTransition: 'slide',  // It can be plain, fade or slide
        bgColor: 'red',              // Background color for toast
        textColor: '#fff',            // text color
        allowToastClose: false,       // Show the close button or not
        hideAfter: 5000,              // `false` to make it sticky or time in miliseconds to hide after
        stack: 5,                     // `fakse` to show one stack at a time count showing the number of toasts that can be shown at once
        textAlign: 'left',            // Alignment of text i.e. left, right, center
        position: 'top-center'       // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values to position the toast on page
    })
}
function msgOK(msg) {
    $.toast({
        text: msg,
        showHideTransition: 'slide',  // It can be plain, fade or slide
        bgColor: 'blue',              // Background color for toast
        textColor: '#fff',            // text color
        allowToastClose: false,       // Show the close button or not
        hideAfter: 5000,              // `false` to make it sticky or time in miliseconds to hide after
        stack: 5,                     // `fakse` to show one stack at a time count showing the number of toasts that can be shown at once
        textAlign: 'left',            // Alignment of text i.e. left, right, center
        position: 'top-center'       // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values to position the toast on page
    })
}
function isReadyAsync(ele, timeOut) {
    
    return new Promise((resolve, reject) => {
        timeOut = timeOut || 500
        var count = Math.floor(timeOut / 10);
        var iCount = 0;
        function run() {
            if (iCount > count) {
                resolve(false);
            }
            else {
                if ($.contains($('body')[0], e[0])) {
                    resolve(true);
                }
                else {
                    iCount++;
                    setTimeout(run, 10);
                }
            }
        }
        run();
    });
}
async function findEleAsync(ele, timeOut) {
    if (await isReady(ele)) {
        return $(ele)
    }
}
/**
 * Parse request qury sang Object
 * Vi du: http://mysite.com?a=1&b=2 retunr {a:1,b:2}
 * *
 * */
function parseUrlParams() {
    if (window.location.href.indexOf('?') == -1) {
        return {}
    }
    var items = window.location.href.split('?')[1].split('&');
    var ret = {}
    items.forEach(function (x) {
        var fx = x.split('=');
        if (fx.length > 1) {
            ret[fx[0].toLocaleLowerCase()] = fx[1]
        }
        else {
            ret[fx[0].toLocaleLowerCase()] = undefined
        }
    });
    return ret;

}
export { parseUrlParams, isReadyAsync, findEleAsync, msgOK, msgError, newScope, postId, BaseView, View, redirect, urlWatching, getModule, getPaths }