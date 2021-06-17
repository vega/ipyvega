import pako = require('pako');
//import buffer = require('buffer');
//var Buffer = buffer.Buffer;
//import lz4 = require('lz4');

export
const decompress : {[key:string]: Function} = {
      zlib: (input: ArrayBuffer): ArrayBuffer => {
           return pako.inflate(new Uint8Array(input)).buffer;
         },
      /*lz4: (input: ArrayBuffer): ArrayBuffer => {
          return lz4.decode(input);
         },*/

}