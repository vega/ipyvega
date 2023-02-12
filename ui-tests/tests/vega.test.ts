// Code adapted from Jupyter Widgets,  Copyright (c) Jupyter Development Team, Distributed under the terms of the Modified BSD License.
// See: https://github.com/jupyter-widgets/ipywidgets/blob/master/ui-tests/tests/widgets.test.ts

import { galata, describe, test } from '@jupyterlab/galata';
import * as path from 'path';

jest.setTimeout(100000);

describe('Vega UI test', () => {
  beforeAll(async () => {
    await galata.resetUI();
    galata.context.capturePrefix = 'vega';
  });

  afterAll(async () => {
    galata.context.capturePrefix = '';
  });

  test('Upload files to JupyterLab', async () => {
    await galata.contents.moveDirectoryToServer(
      path.resolve(__dirname, `./notebooks`),
      'uploaded'
    );
    expect(
      await galata.contents.fileExists('uploaded/NBTest.ipynb')
    ).toBeTruthy();
  });

  test('Refresh File Browser', async () => {
    await galata.filebrowser.refresh();
  });

  test('Open directory uploaded', async () => {
    await galata.filebrowser.openDirectory('uploaded');
    expect(
      await galata.filebrowser.isFileListedInBrowser('NBTest.ipynb')
    ).toBeTruthy();
  });

  test('Run notebook NBTest.ipynb and capture cell outputs', async () => {
    const notebook = 'NBTest.ipynb';
    await galata.notebook.open(notebook);
    expect(await galata.notebook.isOpen(notebook)).toBeTruthy();
    await galata.notebook.activate(notebook);
    expect(await galata.notebook.isActive(notebook)).toBeTruthy();

    let numCellImages = 0;

    const getCaptureImageName = (id: number): string => {
      return `cell-${id}`;
    };

    await galata.notebook.runCellByCell({
      onAfterCellRun: async (cellIndex: number) => {
        const cell = await galata.notebook.getCellOutput(cellIndex);
	console.log("CELL:", cell);
        if (cell) {
          if (
            await galata.capture.screenshot(
              getCaptureImageName(numCellImages),
              cell
            )
          ) {
            numCellImages++;
          }
        }
      },
    });

    for (let c = 0; c < numCellImages; ++c) {
      expect(
        await galata.capture.compareScreenshot(getCaptureImageName(c))
      ).toBe('same');
    }
  });

  test('Close notebook NBTest.ipynb', async () => {
    await galata.notebook.close(true);
  });

});
