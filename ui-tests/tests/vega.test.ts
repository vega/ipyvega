/*
This file contains substantial portions of https://github.com/jupyter-widgets/ipywidgets/blob/7325e5952efb71bd69692b2d7ed815646c0ac521/ui-tests/tests/widgets.test.ts, which has the following license:

     Copyright (c) 2015 Project Jupyter Contributors
     All rights reserved.

     Redistribution and use in source and binary forms, with or without
     modification, are permitted provided that the following conditions are met:

     1. Redistributions of source code must retain the above copyright notice, this
     	list of conditions and the following disclaimer.

     2. Redistributions in binary form must reproduce the above copyright notice,
     	this list of conditions and the following disclaimer in the documentation
   	and/or other materials provided with the distribution.

     3. Neither the name of the copyright holder nor the names of its
        contributors may be used to endorse or promote products derived from
        this software without specific prior written permission.

     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
     AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
     IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
     SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

import { test } from '@jupyterlab/galata';

import { expect } from '@playwright/test';

import * as path from 'path';

test.describe('Widget Visual Regression', () => {
  test.beforeEach(async ({ page, tmpPath }) => {
    await page.contents.uploadDirectory(
      path.resolve(__dirname, './notebooks'),
      tmpPath
    );
    await page.filebrowser.openDirectory(tmpPath);
  });

  test('Run notebook vega.ipynb and capture cell outputs', async ({
    page,
    tmpPath,
  }) => {
    const notebook = 'vega.ipynb';
    await page.notebook.openByPath(`${tmpPath}/${notebook}`);
    await page.notebook.activate(notebook);

    const captures = new Array<Buffer>();
    const cellCount = await page.notebook.getCellCount();

    await page.notebook.runCellByCell({
      onAfterCellRun: async (cellIndex: number) => {
        const cell = await page.notebook.getCellOutput(cellIndex);
        if (cell) {
          captures.push(await cell.screenshot());
        }
      },
    });

    await page.notebook.save();

    for (let i = 0; i < cellCount; i++) {
      const image = `vega-cell-${i}.png`;
      expect(captures[i]).toMatchSnapshot(image);
    }
  });
});