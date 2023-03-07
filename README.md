# MQTT


Paho MQTT client: https://pypi.org/project/paho-mqtt/

Callback-based architecture +

  - `loop_forever`: blocking call, start a main loop,

  - `loop_start`/`loop_stop`: threaded, non-blocking solution.
    Roughly speaking, starts `loop_forever` in a thread.

  - `loop`: not a loop per se, but a blocking single-step "process a bit" that
    you can use in your own loop. Non-threaded, select-based, elementary so
    flexible ; the only point is that we have to make sure that we call it
    frequently enough wrt the `keepalive` setting or we will be disconnected.

    Nota: the documentation states that:

    > It is strongly recommended that you use `loop_start()`, or
    > `loop_forever()`, or if you are using an external event loop using
    > `loop_read()`, `loop_write()`, and `loop_misc()`. 
    > Using `loop()` on it's own is no longer recommended.

    The documentation (https://pypi.org/project/paho-mqtt/#external-event-loop-support)
    is (very) scarce. How wow, this is a low-level, socket-based approach when
    we should do the socket select ourselves! My my!

    The canonical example of this approach is here: https://github.com/eclipse/paho.mqtt.python/blob/master/examples/loop_select.py

    The same low-level approach works with asyncio: https://github.com/eclipse/paho.mqtt.python/blob/master/examples/loop_asyncio.py. Again, this is a thin layer on top of
    select here: we have to get the client socket, register reader and writer with
    `asyncio`, etc. So interface with the socket stuff in asyncio. Jeeez.

    Nota: internally, `loop()` is a simple select-based loop and these 3 functions.
    So that's a good start.



See https://pypi.org/project/paho-mqtt/#loop and the source here: https://github.com/eclipse/paho.mqtt.python/blob/master/src/paho/mqtt/client.py