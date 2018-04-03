import vegaEmbed, { Mode } from 'vega-embed';
import { Spec } from 'vega-lib';
import { TopLevelSpec } from 'vega-lite';

function javascriptIndex(selector, outputs) {
  // Return the index in the output array of the JS repr of this viz
  for (let i = 0; i < outputs.length; i++) {
    const item = outputs[i];
    if (item.metadata &&
      item.metadata['jupyter-vega3'] === selector &&
      item.data['application/javascript'] !== undefined) {
      return i;
    }
  }
  return -1;
}

function imageIndex(selector, outputs) {
  // Return the index in the output array of the PNG repr of this viz
  for (let i = 0; i < outputs.length; i++) {
    const item = outputs[i];
    if (item.metadata &&
      item.metadata['jupyter-vega3'] === selector &&
      item.data['image/png'] !== undefined) {
      return i;
    }
  }
  return -1;
}

export function render(selector, spec: Spec | TopLevelSpec, type: Mode, output_area) {
  console.log('foo')

  // Find the indices of this visualizations JS and PNG
  // representation.
  const imgIndex = imageIndex(selector, output_area.outputs);
  const jsIndex = javascriptIndex(selector, output_area.outputs);

  // If we have already rendered a static image, don't render
  // the JS version or append a new PNG version
  if (imgIndex > -1 && jsIndex > -1 && imgIndex === (jsIndex + 1)) {
    return;
  }

  // Never been rendered, so render JS and append the PNG to the
  // outputs for the cell
  const el = document.getElementById(selector.substring(1));
  vegaEmbed(el, spec, { mode: type }).then(function (result) {
    const imageData = result.view.toImageURL('png').then(function (imageData) {
      if (output_area !== undefined) {
        const output = {
          data: {
            'image/png': imageData.split(',')[1]
          },
          metadata: { 'jupyter-vega3': selector },
          output_type: 'display_data'
        };
        // This appends the PNG output, but doesn't render it this time
        // as the JS version will be rendered already.
        output_area.outputs.push(output);
      }
    }).catch(console.warn);
  }).catch(console.warn);
}
