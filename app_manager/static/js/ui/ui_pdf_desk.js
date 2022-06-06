
import { ui_container } from "./ui_component.js";
import { ui_toolbar } from "./ui_toolbar.js";
import { ui_html } from "./ui_html.js";
import { ui_events } from "./ui_events.js";
import { ui_style } from "./ui_style.js";
import { ui_rect_picker } from "./ui_rect_picker.js";
import { ui_pdf_rect_picker } from "./ui_pdf_rect_picker.js";

const icon_server_browser_file = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAaCAYAAADWm14/AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAARBSURBVEhLvZZZKP1PFMCPfYsoe5YsoZBkKZIoUjxYQ9a8eFRSFMqzUrakvNi3B3mQkCVLSSLxQok8eLMm+3b+c86d73W/XPfy6//7fWqYc2bm3DPne+bMABqhu7sbU1NT0dfXF21sbNDa2hq9vb0xKSkJW1tb8e3tTc78M751ID09HQGAW1VVlbavTxcXF4cvLy9y5e/44sDs7KzW8MrKCusiIyNZTklJwejoaLSzs0N3d3ce293dRUdHRx7v7e1l3W9QOdDR0cGGamtrpQYxJCSEdURpaSnGx8dzn3T29vbcJ9ra2lhXXV0tNT9D68D09DQbmJ+flxrE4uJi7Y8TRUVFHG4FGtOV9/f3WdfV1SU1xjGhP2IRmJiYgAgllJeXw8XFBby/v8PIyAjExMRAREQEvL6+wsLCAtze3kJOTg4tgZOTE1haWoK0tDQQ0QArKyuYnJyE+/t7ODg4gODgYJ5nCHZAZDkbT05OhpubGzAzM4PNzU0ICgoCFxcXeHh4AAsLCxA7hKenJxA5Ac/Pz/yD19fXcHh4CE1NTZCZmQnh4eFsmBw2NzfnvkFkBHBjY4O6THNzsyr0CiUlJdoc+L8AOsuff4zk9vZ2KX2Qm5uLUVFRUtLP+fk5TkxMYF9fH66urkrt90BCQgInl8Ly8rLe3ROGHBgfH+d1SqOipfQpauKTyZlqTLe2tvjbKczMzICbm5uU1IgqCI+Pj1L6gHKioKCAokmec6NEpP+np6ec0JaWlrC4uChXqMHQ0FBMTExEkYTo4ODA55v65LnSqPTS3JaWFnJcizghrDeGEqGdnR2p0cBpKn4UXF1dOWuVRlHQ3S2dAhFWqKmpkRqAsbExEJWQd2qM/Px8ODo64mip5tva2uLQ0BB7Q1RWVmJYWJiU1ExNTcmeBrGcL6TfQGt0ExwotHl5eVJEHB4e5kn6EGde9hDPzs6+nWeI+vp69PPzk5JwgMrmZ0Mkz83NSUk/ouL9kQOicqrWcY8UNKBABYduPEPQZzM1NZXSzxEV9qsDWVlZrKRv7+Pjgx4eHiwHBgaiv78/enl58ekYGBjgRcRnQz+Frmxdx1WXkZOTE9TV1cHl5SXXd7pYxI0IwgG4u7sDZ2dnrvkKtGZvb09b/39CbGwsBAQEwOjoqEbBbgjW19d5R4ODg1KDKAyrdllYWCh7Gihynp6eUjLO1dUV2xMblBr5CRTEueYJZWVlUoOcC4oTomJif38/9xVorKGhQUqGERFTbYhQS4Lt7W2eRI0uFYJygWRx738xcHx8zLrs7Gyp+YoyR2mi0MkRPQ4oVFRUaBdQndA1IL6jnKVBvCFQvCF4LCMjAzs7OzlhGxsbUVRY1lMi69oQ7wxe+60DCpS19CynR6iugZ6eHjnjg7W1Nc4LkawoHiv8nqTCo0DPeV0b9NjVnoJ/hSj9/MIi6B4xGoG/AYWfHi6IiP8BQz+SqTY/EVAAAAAASUVORK5CYII=';
const icon_open_file = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAALcSURBVFhHxZexS3JRFMCPmuUiIrQV2aaLiLpGNEiEi0PgYFMQiEE4iJZgUw2BS0NRDQ6CINJcUIsQ9AcUFE5GQ1ORoqCU0fveOZ0n2nvqs+9ZPzjec+9993ruuefc+55OEIE/RM9lm0qlAjqdbmhZXl7mGYZD5oGtrS04OTmBcrkMLy8v3NqbyclJ8Hq98PDwAOvr63B4eMg9KkEDOkkmk8Ls7CzX1OFwOIRAIIALEfb29rhVHbItQD4/P1lTR6PRgKWlJdo+9GA+n+ceFbAhbcQJhJmZGa6pY3p6mlYvlSj39/fc2x9FDwzL+fk5HBwcwObmJmSzWWq7ubmhchCKQYgufHx8hFKpBE9PT2AwGLhXGZPJBHq9Hux2O1gsFsqKQqEAwWCQn+gD+aEDcRWCzWYjHbuHFWmcaADpg6AtqNVqlHYIrkTi+fkZbm9v4e7ubqCgy+v1Oo8cgu3t7bb1u7u7JJIHfgrOpdoDOzs7MDU1BWdnZxAOhymlfhPy9+rqKvj9fjrVWq0WdSBWqxWMRiMF2SDBrXO73TxSPWP402w2qfKdubk5qFarA7MAeX9/B5fLxTUAs9kM6XQanE4nHVL9EGKxGO9Idxb8FJzz8vJSSCQSpPdDdhCJbaz9Hx8fHzAxMcG13sgMwENEMuL6+hr29/eHTq+1tTXweDxdKd0LioFOpPsdwRjIZDLt/VSzImR+fh4uLi7g6uqK6rlcDl5fX0mXwJjx+Xykd8VA52X09vZGJT4zKunro/HxcYhEIlzTnpWVFeUY6OT4+Jg17cGtUfTAl9cBNjY2qBwFuHpE0QDJC3jHjwpcPSIzAF9Ej46OIJVKcYv2RKNR1r7oyoJisUglto9KOpF5YGFhAeLxONe0B2/f73R5AMG2Ucl3ZB4QvwtY0x6MLSUEMeDYnt9dPSK2gyDe94J41guLi4uyQVrJ6ekp/2U3+PqsOEBLCYVC/Hdy/vjzHOAfpKwT7DEh8XAAAAAASUVORK5CYII=';
const icon_hamburger = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAB+SURBVFhH7ZZRCsAgDEPb3f88/oonmw3U4AWqg+VBsX8JsmT6G9hFnjyvIQMyYEgBaK0hDUcGWgvG0N1xHCNlP/QNjDFyq2fXUhPKAHug986cVg+0FuoBGohrya2eXUs9IAPsgfhBMKfVA62FeoAG4pmUWz27lnpABv5uwGwCidPDHCcveRYAAAAASUVORK5CYII=';
const boxShadow = "rgba(149, 157, 165, 0.2) 0px 8px 24px"
function getUrlOfServerBrowserFileIcon() {
    return q.resources.urlFromImageBase64Text(icon_server_browser_file);
}
class ui_pdf_desk extends ui_container {

    toolbar;
    _hamburger;
    _openFile;
    _pageSelector;
    _zoom;
    _main;
    _pageSelectorThums;
    _desk;
    editor;
    contextMenuOfSelectRegion;
    _extractTextMenuItem;
    _configTextMenuItem;
    _onTesseractRecognize;
    _onBeforeTesseractRecognize;
    style;
    _isCustomToolbar;
    _showThumPage = true;
    _orginSize;

    constructor(ele, isCustomToolbar) {
        
        super();
        this._orginSize = ele.getBoundingClientRect();
        this._isCustomToolbar = isCustomToolbar;
        var R = ele.getBoundingClientRect();
        ele.setAttribute("class", "pdf-picker-editor");
        this.setEle(ele);
        this._initLayout();
        this._initContextMenuOfSelectRegion();
        this._initEvents();

        this._initEditor();
        this.buildStyle();
        this.css({
            height: R.height.toString() + "px",
            width: R.width + "px"
        });
    }
    
    getData() {
        return this.editor.getData();
    }
    getThumbAsFile() {
        return this.editor.getThumbAsFile()
    }
    changeFile() {
        this.editor.changeFile();
    }
    isLocalFile() {
        return this.editor.isLocalFile();
    }
    getFile() {
        return this.editor.getFile();
    }
    loadFile(file, cb) {
        debugger;
        this.editor.loadFromFile(file, cb);
    }
    clear() {
        this.editor.clear();
    }
    loadFromUrl(urlOfFile, fileType, cb) {

        this.editor.loadFromUrl(urlOfFile, fileType, cb);

    }
    buildStyle() {
        this._pageSelectorThums.getEle().setAttribute("class", "page-selector");
        this.style = new ui_style.builder("pdf-picker-editor");
        this.style.define(
            ".pdf-picker-editor .page-selector >img:hover",
            {
                borderColor: "#040b10",
                borderStyle: "solid",
                borderWidth: "2px",
                cursor: "point"
            }
        );
        this.style.define(
            ".pdf-picker-editor .page-selector",
            {
                marginRight: "8px",
                boxShadow: boxShadow,
                overflowY: "auto"
            }
        );
        this.style.define(
            ".pdf-picker-editor .page-selector >img",
            {
                borderColor: "#ccc",
                borderStyle: "solid",
                borderWidth: "2px",
                cursor: "point"
            }
        );
        this.style.define(".pdf-picker-editor .toolbar", {

            height: "48px",
            boxShadow: boxShadow,
            padding: "4px",
            borderBottom: "solid 1px #ccc",
            marginBottom: "8px"
        });
        this.style.define(".pdf-picker-editor .toolbar>div", {
            cursor: "pointer",
            height: "32px",
            padding: "4px"

        });
        this.style.define(".pdf-picker-editor .toolbar > div:has(img)", {
            borderColor: "#ccc",
            borderStyle: "solid",
            borderWidth: "2px",
            height: "22px"
        });
        this.style.applyTo(document.head);

    }
    _initContextMenuOfSelectRegion() {
        this.contextMenuOfSelectRegion = new ui_container();
        this.contextMenuOfSelectRegion.css({
            padding: "10px",
            backgroundColor: "#fff",
            boxShadow: boxShadow
        });
        this.contextMenuOfSelectRegion.getEle().setAttribute("class", "pdf-picker-editor-contex-menu");
        this._extractTextMenuItem = new ui_toolbar.menuItem();
        this._extractTextMenuItem.setText("Nhận dạng");
        this._extractTextMenuItem.setContainer(this.contextMenuOfSelectRegion);
        this._extractTextMenuItem.setCommand("tesseract_recognize");
        this.contextMenuOfSelectRegion.setEvent({
            onclick: evt => {
                var target = evt.target;
                var command = target.getAttribute("command");
                if (command) {
                    this._onCommad(command);
                }
            }
        })
    }
    _initEvents() {
        var me = this;
        if (!this._isCustomToolbar) {
            var pageSelecteorHandle = new ui_events.handler(this._pageSelector.getInput());
            pageSelecteorHandle.set({
                onchange: evt => {
                    var input = evt.target;
                    me.editor.doLoadPage(Number(input.value), () => {
                        me.editor.deskEle.scrollTo({
                            left: 0,
                            top: 0
                        });
                    });
                }
            });
            var zoomhandle = new ui_events.handler(this._zoom.getInput());
            zoomhandle.set({
                onchange: evt => {
                    var input = evt.target;
                    me.editor.doZoom(Number(input.value));
                }
            });

        }
        me._pageSelectorThums.setEvent({
            onclick: evt => {
                var target = evt.target;

                var index = ui_html.getIndexInParent(target) + 1;
                me.loadPage(index);
            }
        });
    }
    loadPage(index, cb) {
        if (!cb) {
            cb = () => { };
        }
        this.editor.doLoadPage(index, cb);
    }
    _initEditor() {
        this.editor = new ui_pdf_rect_picker(this._desk.getEle());
    }

    _initLayout() {
        this.dock();
        this.layoutColumns();
        this.toolbar = new ui_toolbar.h_toolBar()
        this.toolbar.setContainer(this);
        this.toolbar.getEle().setAttribute("class", "tool-bar")
        if (!this._isCustomToolbar) {
            this.toolbar.onCommand(command => {
                this._onCommad(command);
            });
            this.toolbar.getEle().setAttribute("class", "toolbar");
            this._hamburger = new ui_toolbar.toolbarCommandItem();
            this._hamburger.setIconByBase64(icon_hamburger);
            this._hamburger.setCommand("hamrburger");
            this.toolbar.add(this._hamburger);
            this._openFile = new ui_toolbar.toolbarCommandItem();
            this._openFile.setCommand("open-file");
            this._openFile.setIconByBase64(icon_open_file);

            this.toolbar.add(this._openFile);
            this._pageSelector = new ui_toolbar.toolbarInputItem();
            this._pageSelector.setText("Trang");
            ui_html.setAttrs(this._pageSelector.getInput(), {
                type: "number",
                readonly: "readonly",
                min: "1",
                value: "1"
            })
            ui_html.setStyle(this._pageSelector.getInput(), {
                width: "60px"
            });
            this.toolbar.add(this._pageSelector);
            this._zoom = new ui_toolbar.toolbarInputItem();
            this._zoom.setText("Tỉ lệ");
            this._zoom.setAfteText("(%)");
            ui_html.setStyle(this._zoom.getInput(), {
                width: "60px"
            });
            ui_html.setAttrs(this._zoom.getInput(), {
                type: "number",
                width: "60px",
                max: "800",
                step: "10",
                min: "25",
                value: "150"
            });
            this.toolbar.add(this._zoom);


        }
        this._main = new ui_container();
        this._main.setContainer(this);
        this._main.dock();
        this._main.layoutRows();
        this._pageSelectorThums = new ui_container();
        this._pageSelectorThums.css({
            width: "160px",

        });
        this._pageSelectorThums.setContainer(this._main);
        this._desk = new ui_container();
        this._desk.dock();
        this._desk.setContainer(this._main);

    }
    replaceByToolbar(ele) {
        this.toolbar.css({
            display: "none"
        });
        setTimeout(() => {
            this.toolbar.replaceBy(ele);
            this.toolbar.css({
                display: "flex"
            });
        }, 100);

    }
    onTesseractRecognize(cb) {
        this._onTesseractRecognize = cb;

    }
    onBeforeTesseractRecognize(cb) {
        this._onBeforeTesseractRecognize = cb;

    }
    doLoadThumns(width, height) {
        if (this.editor.isPdf) {
            width = width || 80;
            height = height || 80;
            this.editor.loadThumbs(width, height, (url, pageIndex) => {
                var img = ui_html.createEle("img");
                img.setAttribute("src", url);
                img.setAttribute("data-page-index", pageIndex.toString());
                ui_html.setStyle(img, {
                    maxWidth: "112px",
                    margin: "4px"
                });
                this._pageSelectorThums.getEle().appendChild(img);
            });
        }
        else {
            this._pageSelectorThums.getEle().innerHTML = "";
            ui_html.setStyle(this._pageSelectorThums.getEle(), {
                display: "none"

            });
        }
    }
    /**
     * Bắt trình duyệt mở 1 file
     * */
    async doBrowseFileAtClient() {
        return await this.editor.doBrowserFile();
    }
    setShowThumbPage(value) {
        this._showThumPage = value;
        if (this._showThumPage) {
            this._pageSelectorThums.css({
                display: "flex"
            });
        }
        else {
            this._pageSelectorThums.css({
                display: "none"
            });
        }
        this.editor._fixSizeOfEditor();

    }
    _onCommad(command) {
        debugger;
        if (command == "open-file") {
            this._pageSelector.getInput().setAttribute("value", "1");
            var pageIndex = Number(this._pageSelector.getInput().getAttribute("value"));
            this.editor.browseFile(sender => {
                this._pageSelector.setAfteText("/" + sender.numPages);
                sender.doLoadPage(pageIndex, () => {
                    this._pageSelector.getInput().removeAttribute("readonly");
                    this._pageSelector.getInput().setAttribute("max", sender.numPages.toString())
                    this._pageSelectorThums.getEle().innerHTML = "";
                    if (this._showThumPage) {
                        sender.loadThumbs(80, 80, (url, pageIndex) => {
                            var img = ui_html.createEle("img");
                            img.setAttribute("src", url);
                            img.setAttribute("data-page-index", pageIndex.toString());
                            ui_html.setStyle(img, {
                                maxWidth: "112px",
                                margin: "4px"
                            });
                            this._pageSelectorThums.getEle().appendChild(img);
                        });
                    }
                });

            });
        }
        if (command == "tesseract_recognize") {

            ui_html.setStyle(this.editor.getCurrentRegion().canvas, {
                cursor: "wait"
            });
            if (this._onBeforeTesseractRecognize) {
                try {
                    this._onBeforeTesseractRecognize(this.editor.getCurrentRegion());
                } catch (e) {
                    console.error(e);
                }
            }
            this.editor.getCurrentRegion().tesseract_recognize((err, data) => {

                ui_html.setStyle(this.editor.getCurrentRegion().canvas, {
                    cursor: "default"
                });
                if (this._onTesseractRecognize) {
                    if (err) {
                        this._onTesseractRecognize(err, undefined);
                    }
                    else {
                        
                        this._onTesseractRecognize(undefined, { text: data.data.text, data: data.data });
                    }
                }
                else {
                    this.showRecognize(err, data);;
                }
            });
        }
    }
    showRecognize(err, data) {
        this.editor.getCurrentRegion().show_tesseract_recognize(data.data);

    }
    onLoadComplete(cb) {
        this.editor.onLoadComplete(cb);
    }
    
    async doZoom(percenrRate) {
        await this.editor.doZoom(percenrRate);
    }
    /**
     * Tạo context menu cho vùng đang edit
     * dựa vào một DOM
     * context Menu cho vùng đang edit là gì?
     * Trong quá trình biên tập Region trên file PDF hoặc file Image
     * Người dùng có thể tạo ra nhiều Region và ở 1 thời điểm nhất định 
     * chỉ có 1 region đang được edit gọi là Editing Region.
     * Khi người dùng kích phím phải của Mouse ngay tại Editing Region thẻ DIV trong tham số sẽ hiển thị đúng
     * vị trí của Mouse
     * Context Menu này sẽ áp dụng ngay trên trên Editing Region
     * Điều này có nghĩa là bạn phải tạo một thể DIV trong layout
     * Rồi dùng Jquery hoặc document.getElement để trut cập đến DOM của DIV
     * Rồi gọi hàm setContextMenuOfSelectRegion với tham số là DOM element 
     * @param {any} eleMenu
     */
    setContextMenuOfSelectRegion(eleMenu) {
        this.editor.setContextMenuOfSelectRegion(eleMenu);
    }
    getSelection() {
        return this.editor.getSelection();
    }
    tesseractRecognizeText(cb) {
        this.editor.tesseract_recognize(this.editor.getCurrentRegion(), (err, data) => {
            if (err) {
                cb(err, undefined);
            }
            else {
                cb(undefined, data.data);
            }
        });
    }
    createRegion(data) {
        return this.editor.createRegion(data);
    }
    loadData(dataArray) {
        this.editor.loadData(dataArray);
    }
    /**
     * Sự kiện on select Region để Edit
     * asyncCallback phải là async function
     * @param {any} asyncCallback
     */
    onSelectPicker(asyncCallback) {
        this.editor.onSelectPicker(asyncCallback);
    }
    /**
     * Khi người dùng nhấn ctrl và select
     * @param {any} asynCallback
     */
    onCtrlSelect(asynCallback) {
        this.editor.onCtrlSelect(asynCallback);
    }
}
export { ui_pdf_desk}