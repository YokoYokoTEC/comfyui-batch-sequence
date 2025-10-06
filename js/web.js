import {api} from '../../scripts/api.js';
import {app} from '../../scripts/app.js';

async function disable(dst, fb) {
  dst.disabled = fb;
}

app.registerExtension({
  name: 'comfyui-batch-sequence',
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === 'BatchCounter|YokoYokoTEC') {
      const origOnNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function() {
        const r = origOnNodeCreated ? origOnNodeCreated.apply(this) : undefined;
        for (const w of this.widgets) {
          if (w.name === 'control_after_generate') {
            w.value = w.options.values[1];
          }
        }
        return r;
      }
    }
    // ──────────────────────────
    if (nodeData.name === 'LineRead|YokoYokoTEC') {
      const onAdded = nodeType.prototype.onAdded;
      nodeType.prototype.onAdded = function() {
        const r = onAdded?.apply(this, arguments);
        for (const w of this.widgets) {
          if (w.name === 'file') {
            let lastValue;
            async function Changed(src, dst) {
              await disable(dst, true);
              // ──────────────────────────
              let url = '/YokoYokoTEC/LinRead/' + src.value;
              const res = await (await api.fetchApi(url)).json();
              // ──────────────────────────
              dst.options.values = []
              dst.options.values = res;
              const valid = dst.options.values.includes(dst.value);
              if (!valid) {
                dst.value = dst.options.values[0];
              }
              // ──────────────────────────
              await disable(dst, false);
              app.graph.setDirtyCanvas(true, false);
            }
            // ──────────────────────────
            const src = this.widgets.find((w) => w.name === 'path');
            const cb = src.callback;
            src.callback =
                function() {
              const v = cb?.apply(this, arguments) ?? src.value;
              if (v !== lastValue) {
                lastValue = v;
                Changed(src, w);
              }
              return v;
            }
            // ──────────────────────────
            lastValue = src.value;
            Changed(src, w);
            lastValue = src.value;
          }
        }
        return r;
      }
    }
  }
})
