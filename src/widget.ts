import { DOMWidgetView } from "@jupyter-widgets/base";
import { vegaEmbed } from "./index";
import { Result } from "vega-embed";

interface WidgetUpdate {
  key: string;
  remove?: string;
  insert?: any[];
}

interface WidgetUpdateMessage {
  type: "update";
  updates: WidgetUpdate[];
}

// validate the ev object and cast it to the correct type
function checkWidgetUpdate(ev: any): WidgetUpdateMessage | null {
  if (ev.type != "update") {
    return null;
  }

  // TODO: Fully validate ev and give a easy to understand error message if it is ill-formed
  return ev as WidgetUpdateMessage;
}

export class VegaWidget extends DOMWidgetView {
  result?: Result;
  viewElement = document.createElement("div");
  errorElement = document.createElement("div");

  render() {
    this.el.appendChild(this.viewElement);
    this.errorElement.style.color = "red";
    this.el.appendChild(this.errorElement);

    const reembed = async () => {
      const spec = JSON.parse(this.model.get("_spec_source"));
      const opt = JSON.parse(this.model.get("_opt_source"));

      if (spec == null) {
        return;
      }

      try {
        const result = await vegaEmbed(this.viewElement, spec, {
          loader: { http: { credentials: "same-origin" } },
          ...opt,
        });
        if (this.result) {
          this.result.finalize();
        }
        this.result = result;
        this.send({ type: "display" });
      } catch (err) {
        if (this.result) {
          this.result.finalize();
        }
        console.error(err);
      }
    };

    const applyUpdate = async (update: WidgetUpdate) => {
      const result = this.result;
      if (result == null) {
        throw new Error("Internal error: no view attached to widget");
      }

      const filter = new Function(
        "datum",
        "return (" + (update.remove || "false") + ")"
      );
      const newValues = update.insert || [];
      const changeSet = result.view
        .changeset()
        .remove(filter)
        .insert(newValues);

      await result.view.change(update.key, changeSet).runAsync();
    };

    const applyUpdates = async (message: WidgetUpdateMessage) => {
      for (const update of message.updates) {
        await applyUpdate(update);
      }
    };

    this.model.on("change:_spec_source", reembed);
    this.model.on("change:_opt_source", reembed);
    this.model.on("msg:custom", (ev: any) => {
      const message = checkWidgetUpdate(ev);
      if (message == null) {
        return;
      }

      applyUpdates(message).catch((err: Error) => {
        this.errorElement.textContent = "" + err;
        console.error(err);
      });
    });

    // initial rendering
    reembed();
  }
}
