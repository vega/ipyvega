import vegaEmbed, { Mode, EmbedOptions } from "vega-embed";
import { Spec, View } from "vega";
import { TopLevelSpec } from "vega-lite";

export { default as vegaEmbed } from "vega-embed";

function javascriptIndex(selector: string, outputs: any) {
  // Return the index in the output array of the JS repr of this viz
  for (let i = 0; i < outputs.length; i++) {
    const item = outputs[i];
    if (
      item.metadata &&
      item.metadata["jupyter-vega"] === selector &&
      item.data["application/javascript"] !== undefined
    ) {
      return i;
    }
  }
  return -1;
}

function imageIndex(selector: string, outputs: any) {
  // Return the index in the output array of the PNG repr of this viz
  for (let i = 0; i < outputs.length; i++) {
    const item = outputs[i];
    if (
      item.metadata &&
      item.metadata["jupyter-vega"] === selector &&
      item.data["image/png"] !== undefined
    ) {
      return i;
    }
  }
  return -1;
}

function showError(el: HTMLElement, error: Error) {
  el.innerHTML = `<div class="error">
    <p>Javascript Error: ${error.message}</p>
    <p>This usually means there's a typo in your chart specification.
    See the JavaScript console for the full traceback.</p>
  </div>`;

  throw error;
}

export function render(
  selector: string,
  spec: Spec | TopLevelSpec,
  type: Mode,
  opt: EmbedOptions,
  output_area: any
) {
  // Find the indices of this visualizations JS and PNG
  // representation.
  const imgIndex = imageIndex(selector, output_area.outputs);
  const jsIndex = javascriptIndex(selector, output_area.outputs);

  // If we have already rendered a static image, don't render
  // the JS version or append a new PNG version
  if (imgIndex > -1 && jsIndex > -1 && imgIndex === jsIndex + 1) {
    return;
  }

  // Never been rendered, so render JS and append the PNG to the
  // outputs for the cell
  const el = document.getElementById(selector.substring(1));
  vegaEmbed(el, spec, {
    loader: { http: { credentials: "same-origin" } },
    ...opt,
    mode: type
  })
    .then(result => {
      result.view
        .toImageURL("png")
        .then(imageData => {
          if (output_area !== undefined) {
            const output = {
              data: {
                "image/png": imageData.split(",")[1]
              },
              metadata: { "jupyter-vega": selector },
              output_type: "display_data"
            };
            // This appends the PNG output, but doesn't render it this time
            // as the JS version will be rendered already.
            output_area.outputs.push(output);
          }
        })
        .catch(error => showError(el, error));
    })
    .catch(error => showError(el, error));
}

// NOTE: juggle to support optional dependencies that don't break webpack and jupyter
var VegaWidgetDef: any = null;
if (__webpack_modules__[require.resolveWeak("@jupyter-widgets/base")]) {
  const widgets = require("@jupyter-widgets/base");

  VegaWidgetDef = widgets.DOMWidgetView.extend({
    render: function() {
      const reembed = () => {
        this.view = null;
        const spec = JSON.parse(this.model.get("_spec_source"));

        if (spec == null) {
          return;
        }

        vegaEmbed(this.el, spec)
          .then(({ view }) => {
            this.view = view;
          })
          .catch(err => console.error(err));
      };

      this.model.on("change:spec_source", reembed);
      this.model.on("msg:custom", (ev: any) => {
        if (ev.type != "update") {
          return;
        }
        if (this.view == null) {
          console.error("no view attached to widget");
          return;
        }

        const filter = new Function(
          "datum",
          "return (" + (ev.remove || "false") + ")"
        );
        const newValues = ev.insert || [];

        const changeSet = this.view
          .changeset()
          .insert(newValues)
          .remove(filter);
        this.view.change(ev.key, changeSet).run();
      });

      // initial rendering
      reembed();
    }
  });
}

export const VegaWidget = VegaWidgetDef;
