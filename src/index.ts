import { Spec } from "vega";
import vegaEmbed, { EmbedOptions, Mode } from "vega-embed";
import { TopLevelSpec } from "vega-lite";

export { default as vegaEmbed } from "vega-embed";
export { VegaWidgetModel, VegaWidget } from "./widget";
export const version = require("../package.json").version;

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
  if (imgIndex > -1 && jsIndex > -1) {
    return;
  }

  // Never been rendered, so render JS and append the PNG to the
  // outputs for the cell
  const el = document.getElementById(selector.substring(1))!;
  vegaEmbed(el, spec, {
    loader: { http: { credentials: "same-origin" } },
    ...opt,
    mode: type,
  })
    .then((result) => {
      result.view
        .toImageURL("png")
        .then((imageData) => {
          if (output_area !== undefined) {
            const output = {
              data: {
                "image/png": imageData.split(",")[1],
              },
              metadata: { "jupyter-vega": selector },
              output_type: "display_data",
            };
            // This appends the PNG output, but doesn't render it this time
            // as the JS version will be rendered already.
            output_area.outputs.push(output);
          }
        })
        .catch((error) => showError(el, error));
    })
    .catch((error) => showError(el, error));
}

export * from "./widget";
