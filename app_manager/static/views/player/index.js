
import { BaseScope, View } from "./../../js/ui/BaseScope.js";
var playerView = await View(import.meta, class PlayerView extends BaseScope {
    data = {}
    async playByItem(item) {
        this.data = item;
        this.$applyAsync();
        var me = this;
        await this.onResize(async (w, h) => {
           
           
            var jQVideo = await me.$findEle("video");
            jQVideo.attr("width", w)
            jQVideo.attr("height", h)
        });
        
    }
});
export default playerView;