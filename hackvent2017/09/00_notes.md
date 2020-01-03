Day 09: JSONion
===============
> ... is not really an onion. Peel it and find the flag.

The zip file once decompressed contains an ascii file with JSON data inside. The first layer contains an array with one object and four keys: `op`, `content`, `mapFrom` and `mapTo`. Once you figure out that you have to decode the content using the operator and that map is a substitution the rest follows. Dcode the first layer to get another operator and then recursively decode each layer in turn with the appropriate operator until you get the flag. The operator used were:

- map, character substitution
- gzip, gzip compression
- b64, base 64 encoding
- nul, nothing, just take the inner object
- xor, xor between the content and the mask
- rev, reverse the content

**Warning**, in the process I forgot that there could be more than one object in a JSON array and blindly went through using the first element in the array... which leads to a decoy flag. At one point there are two elements in the array and one should take the second.

The script is used is pasted below:
```python
#!/usr/bin/python3

from json import load, loads
from gzip import decompress
from base64 import b64decode
from itertools import cycle

def peel_list(l, count):
        return([peel_layer(layer, count) for layer in l])

# recursively decode layers
def peel_layer(layer, count):
        op = layer['op']
        print('Decoding layer {} with operator {}.'.format(count, op))
        if op == 'map':
                # map is a simple character substitution, create the mapping and apply it
                subst = dict(zip([c for c in layer['mapFrom']], [c for c in layer['mapTo']]))
                result = ''.join([subst[c] for c in layer['content']])
                return(peel_list(loads(result), count+1))
        elif op == 'gzip':
                # gzip encoded data, just decode it
                result = decompress(b64decode(layer['content']))
                return(peel_list(loads(result), count+1))
        elif op == 'b64':
                # just decode b64 data
                result = b64decode(layer['content'])
                return(peel_list(loads(result), count+1))
        elif op == 'nul':
                # nothing to do, get content
                result = layer['content']
                return(peel_list(loads(result), count+1))
        elif op == 'xor':
                # apply xor on content and a repetition of the mask
                result = bytes(b1^b2 for b1, b2 in zip(b64decode(layer['content']), cycle(b64decode(layer['mask']))))
                return(peel_list(loads(result), count+1))
        elif op == 'rev':
                # reverse the content using extended slice
                result = layer['content'][::-1]
                return(peel_list(loads(result), count+1))

        return(layer)

# load the JSON data from the file
def load_onion():
        f = open('jsonion.json', 'r')
        onion = load(f)
        f.close()
        return onion

if __name__ == "__main__":
        # load data
        onion = load_onion()

        # peel recursively
        result = peel_list(onion, 0)
        print(result)
```

In the end, one gets the flag:
```
HV17-Ip11-9CaB-JvCf-d5Nq-ffyi
```
