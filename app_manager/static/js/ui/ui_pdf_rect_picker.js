import { ui_html } from "./ui_html.js";
import { ui_graph2d } from "./ui_graph2d.js";
import { ui_desk } from "./ui_desk.js"
import { ui_events } from "./ui_events.js"
import { ui_rect_picker } from "./ui_rect_picker.js";
import { ui_linear } from "./ui_linear.js";
class ui_pdf_rect_picker {

    _accept = "image/*,application/pdf";
    SCALE_BUFFER_SIZE = 2;
    bufferCanvas = {};

    async changeFile() {
        var me = this;
        var f = await ui_html.browserFile(this._accept);
        var urlOfFile = URL.createObjectURL(f);
        this._File = f;
        var fileType = f.type;
        this._originFile = f;
        try {
            var me = this;

            me.urlOfFile = urlOfFile;

            me.fileType = (fileType == null || fileType == undefined) ? "" : fileType;
            if (me.fileType.indexOf("image/") > -1) {
                me.isPdf = false;

                me.pdf = undefined;

                if (me.fileType == "image/tiff") {
                    ui_graph2d.convertTIFToPngFile(me._originFile).then(f => {
                        me._File = f;
                        me._originFile = f;
                        me.urlOfFile = URL.createObjectURL(f);
                        me.fileType = "image/png";
                        me.doLoadImage((s) => {
                            resolve(s);
                        });
                    }).catch(ex => {
                        reject(ex);
                    });
                }
                else {

                    me.doLoadImage((s) => {
                        resolve(s);
                    });
                }

            }
            else {

                me.isPdf = true;
                var loadingTask = window["pdfjsLib"].getDocument(me.urlOfFile);
                var pdf = await loadingTask.promise();
                me.numPages = Number(pdf.numPages);
                me.pdf = pdf;
                await me.doLoadPage(1);
                var pdf = await loadingTask.promise();
                return me;

            }
        } catch (e) {
            if (me._onError) {
                me._onError(e);
            }
            else {
                console.error(e);
            }

           
        }
    }

    getOriginalCanvas() {
        return this._orginalImageCanvas;
    }
    isLocalFile() {
        return this.urlOfFile.indexOf("blob:") == 0;
    }
    getFile() {

        if (!this.isLocalFile()) {
            return this._File;
        }
        else {
            return this._originFile;
        }
    }
    _isOnZoomPhase;
    _orginalImageCanvas;

    _originFile;


    /**
     * Sự kiện on select Region để Edit
     * asyncCallback phải là async function
     * @param {any} asyncCallback
     */
    onSelectPicker(asyncCallback) {
        this._onSelectPicker = asyncCallback;
    }
    _File;
    async getThumbAsFile() {
        var imageData = ui_graph2d.getImage(this.canvas);
        var newImageData = ui_graph2d.scaleImageData(imageData, 0.2);

        return await ui_graph2d.createFileFromImageData(newImageData, "thumbs");

    }
    getZoomValue() {
        return this.zoom;
    }
    _onLoadComplete;
    onLoadComplete(cb) {
        this._onLoadComplete = cb;

    }


    tesseract_recognize_scaleUp = 8;
    getPdfObject() {
        return this.pdf;
    }



    _layers;
    interact;

    detectOnResizePickerEvent;
    currentResizeHandle;
    contextMenuPickerEle;
    contextMenuPickerEvent;

    currentContextMenuContextEvent;
    _onSelectPicker;
    _onAfterEdit;

    _onError;
    _recognizeLanguage = "vie";
    resultWindow;
    resultTextarea;
    fileType;
    isPdf;
    drawEvent;
    deskEle;
    selectorEvent;
    windKeyEvent;



    getScaleValue() {
        return this.zoom;
    }
    getCurrentPageIndex() {
        return this.currentPage;
    }
    zoom = 150;
    //document: HTMLDocument;
    //body: HTMLElement;

    editRegion;
    pageOfPickers = [];
    listOfPickers = [];
    currentPicker;

    numPages = 0;
    history = [];
    trashContainer;

    data;
    urlOfFile;
    pdf;
    canvas;
    ctx;
    currentPage = 1;
    numOfPageRollup = 10;
    //window: Window;

    contextMenuOfSelectRegionRect;

    listOfImageData = [];
    events;
    _onContextMenu;
    constructor(ele) {
        var me = this;
        me.trashContainer = ui_html.createEle("div");
        me.interact = new ui_desk.desk_interact(me);
        me._layers = new ui_desk.desk_layers(me, ele);
        me._layers.drawLayer.disable();
        me._layers.dragLayer.disable();
        console.log(me._layers.dragLayer);
        me._layers.resizeLayer.disable();
        me._layers.zoomLayer.disable();
        me._layers.drawLayer.onStart(() => {
            this.interact.type = ui_desk.desk_interact_emum.draw;
        });
        me._layers.drawLayer.onEnd((R, div) => {


            var picker = new ui_rect_picker(
                R.x,
                R.y,
                R.width,
                R.height
            );

            this._layers.layerBkgEle.appendChild(picker.canvas);

            this.addPicker(picker);
            this._oldCurrentPicker = this.currentPicker;
            this.currentPicker = picker;

            this.select(picker);

        });
        me._layers.dragLayer.onEnd((R, picker) => {
            this._layers.layerBkgEle.appendChild(picker);
            this.currentPicker.x = R.x * (100 / this.zoom);
            this.currentPicker.y = R.y * (100 / this.zoom);
            this.currentPicker.drawWithHandle();
            
            this._raiseOnSelectePicker().then();
        });

        this.windKeyEvent = new ui_events.handler(window);

        
        this._layers.resizeLayer.onStart(() => {
            this.hideContextMenuOfSelecetRegion();
            this._layers.drawLayer.disable();
            this._layers.zoomLayer.disable();
        });
        this._layers.resizeLayer.onReszie((r, ele) => {
            this.currentPicker.x = r.x * 100 / this.zoom;
            this.currentPicker.y = r.y * 100 / this.zoom;
            this.currentPicker.w = r.width * 100 / this.zoom;
            this.currentPicker.h = r.height * 100 / this.zoom;
            this.currentPicker.drawWithHandle();
            this._layers.drawLayer.disable();
            this._layers.zoomLayer.disable();

        });
        this._layers.resizeLayer.onEnd((r, ele) => {
            this.currentPicker.x = r.x * 100 / this.zoom;
            this.currentPicker.y = r.y * 100 / this.zoom;
            this.currentPicker.w = r.width * 100 / this.zoom;
            this.currentPicker.h = r.height * 100 / this.zoom;
            this._layers.layerBkgEle.appendChild(ele);
            this.currentPicker.drawWithHandle();
            //this._layers.drawLayer.enable();
            //this._layers.zoomLayer.enable();
            console.log("this._layers.resizeLayer.onEnd");
            this._raiseOnSelectePicker();
        });
        this._layers.zoomLayer.setConstraint(evt => {
            return evt.ctrlKey;
        });
        this._layers.zoomLayer.onEnd((R, ele) => {
            if (this._asyncOnCtrlSelect) {
                this._asyncOnCtrlSelect(R, ele, this).then();
            }
            

        });
        this.detectOnResizePickerEvent = new ui_events.handler(this._layers.layerBkgEle);
        this.detectOnResizePickerEvent.set({
            filter: evt => {
                return evt.which == 0 && this.currentPicker != undefined;
            },
            onmousemove: evt => {
                var pos = ui_html.getClientCoordinate(evt, this._layers.layerBkgEle);
                var resizeHandle = this.currentPicker.detectResizeHandle(pos);
                this.currentResizeHandle = resizeHandle;
                if (resizeHandle) {
                    ui_html.setStyle(this._layers.layerBkgEle, {
                        cursor: resizeHandle.cursor
                    });

                }
                else {
                    ui_html.setStyle(this._layers.layerBkgEle, {
                        cursor: "default"
                    });
                    this._layers.resizeLayer.disable();
                }
            }
        });
        new ui_events.handler(this._layers.layerBkgEle).set({
            filter: (evt => { return evt.which == 1 && this.currentResizeHandle != undefined }),
            onmousedown: evt => {
                this._layers.resizeLayer.startResize(evt, this.currentPicker.canvas, this.currentResizeHandle.cursor);
                this._layers.dragLayer.disable();
                this._layers.zoomLayer.disable();

            }
        });


        this.selectorEvent = new ui_events.handler(me._layers.layerBkgEle);
        this.selectorEvent.set({
            filter: (evt) => {

                return evt.which == 1 && evt.keyCode == undefined && this.currentResizeHandle == undefined;
            },

            onmousemove: evt => {
                if (this.interact.type != ui_desk.desk_interact_emum.none) {
                    //this._layers.drawLayer.disable();
                }
            },
            onmouseup: evt => {
                me._layers.drawLayer.disable();
                me._layers.dragLayer.disable();
            },
            onmousedown: evt => {
                me.applyHookKey();
                if (!evt.ctrlKey) {
                    var canvas = evt.target;
                    var picker = this.findPickerByCanvas(canvas);
                    if (canvas.tagName == "CANVAS" && picker) {

                        this.currentPicker = picker;
                        this.drawAllPickerWithoutHandle();
                        this.currentPicker.drawWithHandle();
                        me.select(this.currentPicker);
                        me._layers.drawLayer.disable();
                        me.hideContextMenuOfSelecetRegion();
                        me._layers.dragLayer.startDrag(evt, this.currentPicker.canvas);
                    }
                    else {

                        me._layers.drawLayer.startDraw(evt);
                        me._layers.dragLayer.disable();
                    }

                }
                else {
                    me._layers.drawLayer.disable();
                    me._layers.dragLayer.disable();
                    this._layers.zoomLayer.startDraw(evt);
                }
            }
        });
        new ui_events.handler(window, {
            onclick: evt => {

                if (me._layers.layerBkgEle.contains(evt.target)
                    || evt.target == me._layers.layerBkgEle
                    || evt.target == me._layers.ele
                ) {

                    this.applyHookKey();
                }
                else {
                    this.windKeyEvent.unset({ onkeydown })
                }

            }
        });

    }
    /**
     * Khi người dùng nhấn ctrl và select
     * @param {any} asynCallback
     */
    onCtrlSelect(asynCallback) {
        this._asyncOnCtrlSelect = asynCallback;
    }
    async _raiseOnSelectePicker() {
        if (this.__oldCurrentPicker != this.currentPicker) {
            this.hideContextMenuOfSelecetRegion();
            this.__oldCurrentPicker = this.currentPicker;
        }
        if (this._onSelectPicker) {
            await this._onSelectPicker(this.currentPicker);
        }
    }
    applyHookKey() {
        this.windKeyEvent.set({
            onkeydown: evt => {
                if (evt.keyCode == 46) {
                    
                    if (this.currentPicker) {
                        this.delete(this.currentPicker);
                    }
                }
            }
        });
    }

    createTestPicker() {
        var picker = new ui_rect_picker(
            50, 50, 120, 40

        );

        this._layers.layerBkgEle.appendChild(picker.canvas);

        this.addPicker(picker);
        this.currentPicker = picker;
    }
    getData() {
        
        var ret = [];
        this.pageOfPickers.forEach(p => {
            if (p.pickers.length > 0 && p.pageIndex !== undefined && p.pageIndex > 0) {
                var items = [];
                p.pickers.forEach(r => {
                    var rs = new q.desk.regionSelection();
                    rs.x = r.x;
                    rs.y = r.y;
                    rs.width = r.w;
                    rs.height = r.h;
                    rs.meta = r.meta;
                    items.push(rs);
                });
                var pr = new q.desk.pageRegionSelection();
                pr.pageIndex = p.pageIndex;
                pr.regions = items;
                ret.push(pr);
            }
        });
        return ret;
    }
    getSelection() {
        return this.currentPicker;
    }


    loadAllPickersToDesk() {

        for (var i = 0; i < this.listOfPickers.length; i++) {
            this.listOfPickers[i].loadTo(this._layers.layerBkgEle);
            //this.listOfPickers[i].drawWithHandle();
            this.listOfPickers[i].drawWithoutHandle();
        }
    }
    loadData(lst) {
        this.clearAllDisplayPickers();
        this.pageOfPickers = [];
        this.currentPage = 1;
        var me = this;
        lst.forEach(P => {
            try {
                var pOP = new ui_desk.page_of_picker();;
                pOP.pageIndex = P.pageIndex;
                pOP.pickers = [];
                P.regions.forEach(r => {

                    var picker = new ui_rect_picker(r.x, r.y, r.width, r.height);
                    picker.desk = me;
                    picker.scaleSize = this.zoom / 100;
                    picker.setData(r);
                    picker.meta = r.meta;

                    pOP.pickers.push(picker);

                });
                me.pageOfPickers.push(pOP);
            } catch (e) {
                console.error(`please call doLoadData like:
                            editor.doLoadData([
                                    {
                                            pageIndex:<number>,
                                            regions:[
                                                    {
                                                      x:<number>,
                                                      x:<number>,
                                                      width:<number>,
                                                      height:<number>
                                                    }
                                                    ]
                                        }

                            ])`)
            }


        });
        if (this.pageOfPickers.length > 0) {
            me.listOfPickers = this.pageOfPickers[0].pickers;
            me.loadAllPickersToDesk();
        }
    }
    async openFileFromClient() {
        debugger;
        var me = this;
        me.reset();
        await me.browseFile();
        me.clearAllDisplayPickers();
        if (me.isPdf) { // if is pdf file just load the first page
            await me.doLoadPage(1);
        }
        else {
            await me.doLoadImage();
        }
    }
    async doLoadImage() {
        
        if (!this._orginalImageCanvas) {
            this._orginalImageCanvas = ui_html.createEle("canvas");
        }
        if (this.isLocalFile()) {
            ui_graph2d.loadUrlOfImageToCanvas(this.urlOfFile, this._orginalImageCanvas, 1);
            ui_graph2d.loadUrlOfImageToCanvas(this.urlOfFile, this.canvas, this.zoom / 100);
            this._fixSizeOfEditor();
            return this;
        }
        else {
            var f = await ui_graph2d.createFileFromUrl(this.urlOfFile);
            this._originFile = f;

            ui_graph2d.loadImageFileToCanvas(f, this._orginalImageCanvas, 1);
            ui_graph2d.loadImageFileToCanvas(f, this.canvas, this.zoom / 100);
            this._fixSizeOfEditor();
            return this;


        }

    }
    _fixSizeOfEditor() {
        var R = this.deskEle.getBoundingClientRect();
        ui_html.setStyle(this._layers.layerBkgEle, {
            width: (R.width).toString() + "px",
            height: (R.height).toString() + "px",
        });
        ui_html.setStyle(this._layers.dragLayer._ele, {
            width: (R.width).toString() + "px",
            height: (R.height).toString() + "px",
        });
        ui_html.setStyle(this._layers.drawLayer._ele, {
            width: (R.width).toString() + "px",
            height: (R.height).toString() + "px",
        });
        ui_html.setStyle(this._layers.resizeLayer._ele, {
            width: (R.width).toString() + "px",
            height: (R.height).toString() + "px",
        });
    }
    setContextMenuOfSelectRegion(ele) {
        var me = this;
        new ui_events.handler(window, {
            oncontextmenu: evt => {
                if (me._layers.layerBkgEle.contains(evt.target)
                    || evt.target == me._layers.layerBkgEle
                    || evt.target == me._layers.ele
                    || (this.currentPicker && this.currentPicker.canvas == evt.target)
                ) {
                    evt.stopImmediatePropagation();
                    evt.preventDefault();
                    return true;
                }
            },
            onclick: evt => {

                if (me._layers.layerBkgEle.contains(evt.target)
                    || evt.target == me._layers.layerBkgEle
                    || evt.target == me._layers.ele
                ) {

                    this.applyHookKey();
                }
                else {
                    this.windKeyEvent.unset({ onkeydown })
                }

            }
        });
        ele.oncontextmenu = evt => {
            evt.stopPropagation();
            evt.stopImmediatePropagation();
            evt.preventDefault();
            return true;
        }
        new ui_events.handler(this._layers.layerBkgEle, {
            filter: evt => { return evt.which == 3; },
            onmousedown: evt => {
                var canvas = evt.target;
                var picker = this.findPickerByCanvas(canvas);
                if (picker) {

                    this.currentPicker = picker;
                    this.drawAllPickerWithoutHandle();
                    this.currentPicker.drawWithHandle();
                    
                    var pos = new ui_linear.vector(evt.clientX, evt.clientY);
                    this.showContextMenuOfSelecetRegion(pos);

                }
                evt.stopImmediatePropagation();
                evt.preventDefault();
            }
        });
        ui_html.setStyle(ele, {
            float: "left",
            display: "none",
            position: "absolute"
        });

        this.contextMenuPickerEle = ele;
        this.contextMenuOfSelectRegionRect = ele.getBoundingClientRect();
        new ui_events.handler(ele, {
            filter: evt => {
                return this.currentPicker != undefined;
            },

            onmouseleave: evt => {
                ui_html.setStyle(this.contextMenuPickerEle, {
                    display: "none"
                });
            },
            onmousemove: evt => {
                document.body.appendChild(ele);
                ui_html.setStyle(this.contextMenuPickerEle, {
                    display: "block"
                });
            }
        });
    }
    hideContextMenuOfSelecetRegion() {
        ui_html.setStyle(this.contextMenuPickerEle, {
            
            display: "none"
           
        });
    }
    showContextMenuOfSelecetRegion(pos) {
        ui_html.setStyle(this.contextMenuPickerEle, {
            left: pos.x + 'px',
            top: pos.y + 'px',
            display: "block",
            zIndex: "20000"
        });
    }
    setModeEdit() {
        this.interact.type = ui_desk.desk_interact_emum.edit;
    }
    setModeScale() {
        this.interact.type = ui_desk.desk_interact_emum.scale;
    }
    getCurrentPageOfPicker() {
        for (var i = 0; i < this.pageOfPickers.length; i++) {
            if (this.pageOfPickers[i].pageIndex == this.currentPage) {
                return this.pageOfPickers[i];
            }
        }
    }
    addPicker(picker) {
        var me = this;
        if (!me.listOfPickers) {
            me.listOfPickers = [];
        }
        if (!me.pageOfPickers) {
            me.pageOfPickers = [];
        }
        var currentPageOfPickers = me.getCurrentPageOfPicker();
        if (!currentPageOfPickers) {
            currentPageOfPickers = new ui_desk.page_of_picker();
            currentPageOfPickers.pageIndex = this.currentPage;
            currentPageOfPickers.pickers = me.listOfPickers;
            this.pageOfPickers.push(currentPageOfPickers);
        }

        me.addToHistory(me.listOfPickers);
        me.listOfPickers.push(picker);
        picker.desk = me;
        picker.setScale(me.zoom / 100);
    }
    addToHistory(listOfPickers) {
        var me = this;
        var newLis = [];
        for (var i = 0; i < this.listOfPickers.length; i++) {
            newLis.push(this.listOfPickers[i]);
        }
        me.history.push(newLis);
    }
    delete(picker) {
        console.log(picker);
        //this.addToHistory(this.listOfPickers);
        //var newList = [];
        //var currentIndex = i;
        //for (var i = 0; i < this.listOfPickers.length; i++) {
        //    if (this.listOfPickers[i] != picker) {
        //        newList.push(this.listOfPickers[i]);

        //    }
        //    else {
        //        currentIndex = i;
        //    }
        //}
        //this.trashContainer.appendChild(picker.canvas);
        //this.listOfPickers = newList;
        //if (currentIndex < this.listOfPickers.length) {
        //    this.currentPicker = this.listOfPickers[currentIndex];
        //    this.currentPicker.drawWithHandle();
        //}
        //else if (currentIndex - 1 < this.listOfPickers.length &&
        //    currentIndex - 1 >= 0) {
        //    currentIndex = currentIndex - 1;
        //    this.currentPicker = this.listOfPickers[currentIndex];
        //    this.currentPicker.drawWithHandle();
        //}
        //var currentPageOfPicker = this.getCurrentPageOfPicker();
        //if (!currentPageOfPicker) {
        //    currentPageOfPicker = new pageOfPicker();
        //    currentPageOfPicker.pageIndex = this.currentPage;

        //}
        //currentPageOfPicker.pickers = this.listOfPickers;
        if (this._layers.drawLayer._ele.childNodes.length == 1) {
            ui_html.setStyle(this._layers.drawLayer._ele.childNodes[0], {
                display: "none"
            });
        }
    }
    async select(picker) {
        if (this.__oldCurrentPicker != this.currentPicker) {
            this.hideContextMenuOfSelecetRegion();
            this.__oldCurrentPicker = this.currentPicker;
        }
        this.drawAllPickerWithoutHandle();
        this.currentPicker = picker;
        this.currentPicker.drawWithHandle();
        if (this._onSelectPicker) {
            await this._onSelectPicker(picker);
        }
    }
    setNumOfPageRollUp(num) {
        this.numOfPageRollup = num;
    }
    unInstallEvents() {
        //var me = this;

        //me.body.onclick = undefined;
        //me.body.onmousedown = undefined;
        //me.body.onmousemove = undefined;
        //me.body.onmouseup = undefined;
    }
    drawAllPickerWithoutHandle() {
        for (var i = 0; i < this.listOfPickers.length; i++) {
            this.listOfPickers[i].drawWithoutHandle();

        }
    }
    findPickerByCanvas(canvas) {
        for (var i = 0; i < this.listOfPickers.length; i++) {
            if (canvas == this.listOfPickers[i].canvas) {
                return this.listOfPickers[i];
            }
        }
    }
    reset() {

        var me = this;
        me.clearAllDisplayPickers();
        me.fileType = undefined;
        me._File = undefined;
        me.currentPicker = undefined;
        me.listOfPickers = [];
        me.pageOfPickers = [];
        if (me.bufferCanvas) {
            Object.keys(me.bufferCanvas).forEach(k => {
                me.bufferCanvas[k].remove();

            });

        }
        me.bufferCanvas = {};
        me.editRegion = undefined;
        me.interact.type = ui_desk.desk_interact_emum.none;

    }
    clear() {
        var me = this;
        me.clearAllDisplayPickers();
        me.fileType = undefined;
        me._File = undefined;
        me._originFile = undefined;
        me.currentPicker = undefined;
        me.listOfPickers = [];
        me.pageOfPickers = [];
        me.editRegion = undefined;
        me.currentPicker = undefined;
        me.interact.type = ui_desk.desk_interact_emum.none;
        me.canvas.getContext("2d").clearRect(0, 0, me.canvas.width, me.canvas.height);
        me._orginalImageCanvas.getContext("2d").clearRect(0, 0, me._orginalImageCanvas.width, me._orginalImageCanvas.height);
    }
    undo() {
        throw "not implement exception"
    }
    clearAllDisplayPickers() {
        var me = this;
        for (var i = 0; i < this.listOfPickers.length; i++) {
            this.trashContainer.appendChild(this.listOfPickers[i].canvas);

        }
    }
    getCurrentRegion() {
        return this.currentPicker;
    }
    async loadFromFile(file) {
        var me = this;
        var _file = file;
        me.urlOfFile = URL.createObjectURL(_file);
        me.fileType = _file.type;
        me._File = file;
        return await me.loadFromUrl(me.urlOfFile, me.fileType);
    }
    async loadFromUrl(urlOfFile, fileType) {
        try {
            var me = this;
            me.reset();
            me.urlOfFile = urlOfFile;
            me.fileType = (fileType == null || fileType == undefined) ? "" : fileType;
            if (me.fileType.indexOf("image/") > -1) {
                me.isPdf = false;

                me.pdf = undefined;
                me.clearAllDisplayPickers();
                if (me.fileType == "image/tiff") {
                    var f = await ui_graph2d.convertTIFToPngFile(me._originFile);
                    me._File = f;
                    me._originFile = f;
                    me.urlOfFile = URL.createObjectURL(f);
                    me.fileType = "image/png";
                    await me.doLoadImage();
                    return {
                        fileName: me._originFile,
                        numPages:1,
                        isPdf: false
                    }
                }
                else {

                    await me.doLoadImage();
                    return {
                        fileName: urlOfFile,
                        numPages: 1,
                        isPdf: false
                    }
                }

            }
            else {

                try {
                    me.isPdf = true;
                    var loadingTask = window["pdfjsLib"].getDocument(me.urlOfFile);
                    var pdf = await loadingTask.promise;
                    me.numPages = Number(pdf.numPages);
                    me.pdf = pdf;
                    await me.doLoadPage(1);
                    me._fixSizeOfEditor();
                    me.clearAllDisplayPickers();
                    me.reset();
                    return {
                        fileName: me.urlOfFile,
                        numPages: me.numPages,
                        isPdf: true
                    }

                } catch (ex) {
                    if (me._onError) {
                        me._onError(ex);
                    }
                    throw ex;
                }

            }
        } catch (e) {
            if (me._onError) {
                me._onError(e);
            }
            else {
                console.error(e);
            }
            
            throw (e);
        }
    }
    getBufferCanvas(pageIndex) {
        return this.bufferCanvas[pageIndex];
    }
    createBufferCanvas(pageIndex) {
        return this.bufferCanvas[pageIndex] = ui_html.createEle("canvas");
    }
    /***
     * Thực hiện browser file trên trình duyệt
     * */
    doBrowserFile() {
        return new Promise(function (resolve, reject) {

            var f = ui_html.createInput("file", {
                display: "none"
            });


            f.setAttribute("accept", "application/pdf,image/*");
            f.onchange = function (evt) {
                resolve(f.files[0])
            }
            f.click();

        });
    }
    async browseFile() {
        
        var me = this;
        var file = await this.doBrowserFile();
        debugger;
        var retInfo = await this.loadFromFile(file);
    }
    _doLoadAllPage(pageIndex) {
        pageIndex = pageIndex || 1;
        return new Promise(function (resolve, reject) {
            if (pageIndex <= this.numPages) {
                this.getPageAsImage(pageIndex, (img) => {


                    this.listOfImageData.push(img);
                    this._doLoadAllPage(cb, onLoadPageComplete, pageIndex + 1);
                    resolve({
                        image: img,
                        pageIndex: pageIndex
                    });
                });
            }
            else {
                resolve();
            }
        });

    }
    async doLoadAllPages() {
        var me = this;
        var startPage = 1;
        this.listOfImageData = [];
        ui_html.setStyle(this.deskEle, {
            cursor: "progress"
        });
        await this._doLoadAllPage();
        var H = 0;
        var W = 0;
        this.listOfImageData.forEach(p => {
            H += p.height;
            if (W < p.width) {
                W = p.width
            }
        });
        ui_html.setStyle(this.canvas, {
            width: W.toString() + "px",
            height: H.toString() + "px"
        });
        me.canvas.width = W;
        me.canvas.height = H;
        me.ctx = me.canvas.getContext("2d");
        var y = 0;
        this.listOfImageData.forEach(p => {
            me.ctx.putImageData(p, 0, y);
            y += p.height;
        });
    }

    async doLoadPage(pageNumber) {
        var me = this;
        pageNumber = Number(pageNumber);
        if (pageNumber > me.numPages && me.isPdf)
            return;
        me.currentPage = pageNumber;

        ui_html.setStyle(me.deskEle, {
            cursor: "wait"
        });
        var currentPageOfPickers = me.getCurrentPageOfPicker();
        if (!currentPageOfPickers) {
            currentPageOfPickers = new ui_desk.page_of_picker();
            currentPageOfPickers.pickers = [];
            me.pageOfPickers.push(currentPageOfPickers);
        }
        me.clearAllDisplayPickers();
        me.listOfPickers = currentPageOfPickers.pickers;
        me.loadAllPickersToDesk();
        var imgData = await me.getPageAsImage(pageNumber);
        var R = me.deskEle.getBoundingClientRect();
        
        ui_html.setStyle(me._layers.layerBkgEle, {

            width: Math.ceil(R.width) + "px",
            height: Math.floor(R.height - 8) + "px"
        });

        ui_html.setStyle(me.canvas, {
            width: imgData.width.toString() + "px",
            height: imgData.height.toString() + "px"
        });
        me.canvas.width = imgData.width;
        me.canvas.height = imgData.height;
        me.ctx = me.canvas.getContext("2d");

        me.ctx.clearRect(0, 0, imgData.width, imgData.height);
        me.ctx.putImageData(imgData, 0, 0);
        ui_html.setStyle(
            me.deskEle, {
            cursor: "default"
        });

        if (me._onLoadComplete) {
            me._onLoadComplete(me);
        }
        me._isOnZoomPhase = false;


    }
    async getPageAsImage(pageNumber) {
        var canvas = ui_html.createEle("canvas");
        var ctx = await this.loadPageToCanvas(canvas, pageNumber);
        var imgData = ctx.getImageData(0, 0, ctx.canvas.width, ctx.canvas.height);
        return imgData;
    }
    async loadPageToCanvas(canvas, pageNumber) {
        try {
            var me = this;
            var data = await ui_graph2d.pdfLoadPage(this.pdf, me.zoom / 100, pageNumber, canvas);
            this.ctx = data.canvasContext;
            return data.canvasContext;

        } catch (err) {
            if (this._isOnZoomPhase) return;
            if (me._onError) {
                me._onError(err);
            }
        }

    }
    async doZoom(zoom) {
        this._isOnZoomPhase = true;

        this.zoom = Number(zoom);

        if (this.pdf) {
            await this.doLoadPage(this.currentPage);
            this.doScaleAllPicker();
        }
        else {

            var imgData = ui_graph2d.getImage(this._orginalImageCanvas);

            var newImgData = ui_graph2d.scaleImageData(imgData, this.zoom / 100);


            ui_html.setStyle(this.canvas, {
                width: Math.ceil(newImgData.width) + "px",
                height: Math.ceil(newImgData.height) + "px",

            });
            this.canvas.width = Math.ceil(newImgData.width);
            this.canvas.height = Math.ceil(newImgData.height);
            var ctx = this.canvas.getContext("2d");


            ctx.putImageData(newImgData, 0, 0);

            this.doScaleAllPicker();

        }

    }
    doScaleAllPicker() {
        this.pageOfPickers.forEach(p => {
            p.pickers.forEach(x => {
                x.scale(this.zoom / 100);
            });
        });

        for (var i = 0; i < this.listOfPickers.length; i++) {
            this.listOfPickers[i].clearDraw();
        }
        for (var i = 0; i < this.listOfPickers.length; i++) {
            this.listOfPickers[i].drawWithoutHandle();
        }
        this.currentPicker = undefined;
    }
    async loadThumbs(w, h) {
        var me = this;
        var result = await me._doLoadAllPage();
        var canvas = ui_html.createEle("canvas");
        canvas.width = imageData.width;
        canvas.height = imageData.height;
        var ctx = canvas.getContext('2d');
        //ctx.scale(scale, scale)
        ctx.putImageData(imageData, 0, 0);
        var blogUrl = ui_resource.urlFromImageBase64Text(canvas.toDataURL("image/png"));
        return new {
            url: blogUrl,
            pageIndex: pageIndex
        };
    }
    setRecognizeLanguage(lang) {
        this._recognizeLanguage = lang;
    }
    onError(cb) {
        this._onError = cb;
    }
    async tesseract_recognize(picker) {
        var me = this;
        var url = await picker.getImageUrl(this.tesseract_recognize_scaleUp);
        var worker = window["Tesseract"].createWorker();
        await worker.load();
        await worker.loadLanguage(me._recognizeLanguage);
        await worker.initialize(me._recognizeLanguage);
        var data = await worker.recognize(url);
        return data;
    }
    createRegion(data, pageNumber) {
        pageNumber = pageNumber || this.currentPage;
        var ret = new ui_rect_picker(data.x, data.y, data.width, data.height);

        ret.scaleSize = 100 / this.zoom;

        ret.setData(data);

        if (pageNumber == this.currentPage) {
            this.addPicker(ret);
            ret.setData(data);
            ret.loadTo(this._layers.layerBkgEle);
            ret.drawWithHandle();
        }

        return ret;
    }
};
export { ui_pdf_rect_picker }