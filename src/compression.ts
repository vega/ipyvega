import pako = require('pako');
import lz4 = require("lz4js");
export
const decompress : {[key:string]: Function} = {
      zlib: (input: ArrayBuffer): ArrayBuffer => {
           return pako.inflate(new Uint8Array(input)).buffer;
         },
      lz4: (input: ArrayBuffer): ArrayBuffer => {
          return lz4.dcompress(new Uint8Array(input)).buffer;
         },

}