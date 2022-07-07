
import { BaseScope, View } from "./../../js/ui/BaseScope.js";
var playerView = await View(import.meta, class PlayerView extends BaseScope {
    data = {}
    async playByItem(item) {
        this.data = item;
        this.$applyAsync();
        var me = this;
        await this.onResize(async (w, h) => {
           
            var ifrm = await me.$findEle("iframe");
            alert(ifrm.length);
            ifrm.attr('src', item.UrlOfServerPath);
            //var jQVideo = await me.$findEle("video");
            //jQVideo.attr("width", w-20)
            //jQVideo.attr("height", h-20)
        });
        
        
    }
});
export default playerView;