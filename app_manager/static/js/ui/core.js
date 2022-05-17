﻿

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
function combine(A, BClass) {
    
    var keys = getAllKeyOfProtoType(A.__proto__).concat(Object.keys(A));
    keys.forEach(function (k) {
        if (!(BClass.prototype[k] && BClass.prototype[k] != null)) {
            BClass.prototype[k] = A[k];
           
        }
    });
    BClass.prototype.$scope = A;
    var B = new BClass();
    var keys = getAllKeyOfProtoType(B.__proto__);
    
    keys.forEach(function (k) {
        
        if (!(A.__proto__[k] && A.__proto__[k] != null)) {
            A.__proto__[k] = B[k];

            
        }
    });
    
    A.__init__(A);
    return A;
}
class BaseView {
    setUrl(url) {
        var metaInfo = JSON.parse(JSON.stringify(url));
        if (metaInfo.url)
            this.url = metaInfo.url;
        else
            this.url = url;

        this.templateUrl = this.url + ".html";

        var urlId = URL.createObjectURL(new Blob([this.templateUrl]));
        var id = urlId.split('/')[urlId.split('/').length - 1];
        this.id = id;

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
    async render(ele) {
        
        var html = await this.getLayoutHtml();
        var compile = angular.element(document.querySelector('[ng-controller]')).injector().get("$compile");
        this.$elements = $("<div class='test'>" + html + "</div>").contents();
        compile(this.$elements)(this);
        this.$elements.appendTo(ele);
        this.$applyAsync();
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
    function applyResolve(scope) {
        scope = scope || angular.element(document.body).scope().$root;

        var subScope = scope.$new(true);
        subScope = combine(subScope, classView)
        subScope.setUrl(url);
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
export { newScope, postId, BaseView, View, redirect }