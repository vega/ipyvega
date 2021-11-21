import * as plugin from "./index";
import * as base from "@jupyter-widgets/base";

module.exports = {
  id: "jupyter-vega",
  requires: [base.IJupyterWidgetRegistry],
  activate: (app: any, widgets: any) => {
    widgets.registerWidget({
      name: "jupyter-vega",
      version: plugin.version,
      exports: plugin,
    });
  },
  autoStart: true,
};
