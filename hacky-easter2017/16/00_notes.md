16 - Pathfinder
---------------
This time we have to find a path, each time we get a page we receive a message that either directs us to go on and try one more step or to turn around because this leads nowhere. It looks like we have to find our way through a maze. To do that I chose to use DFS algorithm, following the graph in depth first. This was done using the following python script:
```python
#!/usr/bin/python3

import urllib.request
import json

def check_path(req):
        resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        print(req.full_url + ' : ' + str(resp))
        if resp['Answer'] == 'This leads to nowhere, so turn around!':
                return False
        elif resp['Answer'] == 'Go on! Follow one of the possible paths' or resp['Answer'] == 'Follow one of the possible paths':
                return resp['paths']
        else:
                print(resp)
                return False

def dfs(req):
        nodes = check_path(req)
        print(nodes)
        if nodes:
                for n in nodes:
                        new_req = urllib.request.Request(req.full_url + str(n), None, {'User-Agent': 'PathFinder'})
                        dfs(new_req)

req = urllib.request.Request('http://hackyeaster.hacking-lab.com:9999/', None, {'User-Agent': 'PathFinder'})
dfs(req)
```

I ran it as `python3 pathfinder.py | tee log.txt` then I searched in the log to find the answer that is different:
```bash
$ cat log.txt | grep -v '^\[.*\]' | grep -v 'This leads to nowhere, so turn around' | grep -v 'Follow one of the possible paths' | grep -v '^False$'
http://hackyeaster.hacking-lab.com:9999/157294683269358174843716529496583712528971346731642895972135468685427931314869257 : {'Answer': 'Thanks PathFinder you saved my life by giving me the solution to this sudoku!', 'Secret': 'https://hackyeaster.hacking-lab.com/hackyeaster/images/challenge/egg16_UYgXzJqpfc.png', 'your_solution': [[1, 5, 7, 2, 9, 4, 6, 8, 3], [2, 6, 9, 3, 5, 8, 1, 7, 4], [8, 4, 3, 7, 1, 6, 5, 2, 9], [4, 9, 6, 5, 8, 3, 7, 1, 2], [5, 2, 8, 9, 7, 1, 3, 4, 6], [7, 3, 1, 6, 4, 2, 8, 9, 5], [9, 7, 2, 1, 3, 5, 4, 6, 8], [6, 8, 5, 4, 2, 7, 9, 3, 1], [3, 1, 4, 8, 6, 9, 2, 5, 7]], 'sudoku': [[0, 0, 0, 2, 0, 4, 6, 0, 0], [2, 0, 9, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 5, 0, 0], [0, 0, 6, 5, 0, 0, 7, 1, 0], [0, 0, 0, 9, 0, 0, 0, 4, 0], [7, 3, 1, 0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 3, 0, 0, 0, 8], [0, 8, 0, 0, 2, 7, 0, 3, 1], [0, 1, 4, 0, 6, 0, 0, 0, 0]]}
{'Answer': 'Thanks PathFinder you saved my life by giving me the solution to this sudoku!', 'Secret': 'https://hackyeaster.hacking-lab.com/hackyeaster/images/challenge/egg16_UYgXzJqpfc.png', 'your_solution': [[1, 5, 7, 2, 9, 4, 6, 8, 3], [2, 6, 9, 3, 5, 8, 1, 7, 4], [8, 4, 3, 7, 1, 6, 5, 2, 9], [4, 9, 6, 5, 8, 3, 7, 1, 2], [5, 2, 8, 9, 7, 1, 3, 4, 6], [7, 3, 1, 6, 4, 2, 8, 9, 5], [9, 7, 2, 1, 3, 5, 4, 6, 8], [6, 8, 5, 4, 2, 7, 9, 3, 1], [3, 1, 4, 8, 6, 9, 2, 5, 7]], 'sudoku': [[0, 0, 0, 2, 0, 4, 6, 0, 0], [2, 0, 9, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 5, 0, 0], [0, 0, 6, 5, 0, 0, 7, 1, 0], [0, 0, 0, 9, 0, 0, 0, 4, 0], [7, 3, 1, 0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 3, 0, 0, 0, 8], [0, 8, 0, 0, 2, 7, 0, 3, 1], [0, 1, 4, 0, 6, 0, 0, 0, 0]]}
```

In there we see the URL to the egg and here it is:  
![](./16/egg16.png)
