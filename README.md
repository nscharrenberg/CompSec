# CompSec

## Installation
### Server
1. Open the `Server` directory as a project in Pycharm.
2. Setup virtualenv on the `Server` directory project.
3. Let it install the required packages in `requirements.txt` when asked.
4. Run `server.py` on the virualenv python interpreter which has the packages.

It should run when it's displaying: `======== Running on http://{HOST}:{PORT} ========` in your terminal.

### Client
1. Open the `Client` directory as a project in Pycharm
2. Set the python interpreter of the client project on the one we setup in `Server`.
3. Now run `single_client_app.py` on the virtualenv python interpreter which has the packages.
3. or run `multiple_client_app.py` on the virtualenv python interpreter which has the packages. (used for our internal testing)

`single_client_app.py` will run one client with the specified json file path.
`multiple_client_app.py` will run the 10 files in the `json_files` directory as a new client each other. (Used for our internal testing)


## Important
For your convenience we've already provided the public & private keys and some dummy data on the program.
Do not remove `private.pem` and `public.pem` unless you know what you are doing.

In case you did remove `private.pem` or `public.pem`, you can run `main.py` in `Server` and it'll store the new keys.
Do make sure to completely clear the `counter.json` and put the below json in the file:
```json
{
    "transactions": []
}
```


## Fix It
We only got one remark on the "Break It" part, which was the network packages could be read as from which plane text could be read.
During the "Build It" process, we were already aware of this issue, as we were not using any SSL/TLS protocols.

During the "Fix It" we therefore implemented WSS and tested using Wireshark whether the network packages could still be read. Which we could not as they were now encrypted.

We also looked at some remarks other groups got and tested them, but for those that we looked at we gave back error messages when constraints were not met.
