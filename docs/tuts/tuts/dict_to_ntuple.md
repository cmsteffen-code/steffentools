Using `dict_to_ntuple`
======================
The `dict_to_ntuple` function is a useful way to turn complex, nested dictionary datatypes into a more coder-friendly nested `namedtuple` format. For example, let's say we're working with the following dictionary:

```
DEMO_DICT = {
    "result": "success",
    "message_list": [
        {"id": 1, "msg": "sam called"},
        {"id": 2, "msg": "he wants his groove back"},
        {"id": 3, "msg": "he thinks you took it"},
    ],
    "errors": [
        "not enough jelly",
        "too much peanut butter",
        "no bread",
    ],
    "nest": {"type": "bowl", "material": "straw"},
}
```

If you wanted to print this information to the screen, you could do this:

```
# Display the contents of the dict.
print(f"Result: {DEMO_DICT['result']}")
print("Messages:")
for message in DEMO_DICT["message_list"]:
    print(f"  {message['id']}: {message['msg']}")
print("Errors:")
for error in DEMO_DICT["errors"]:
    print(f"  {error}")
print(f"Nest: type='{DEMO_DICT['nest']['type']}',"
      f"material='{DEMO_DICT['nest']['material']}'")
```

But with `dict_to_ntuple`, you can convert it to a `namedtuple`, allowing you to access the data in a simpler fashion, which is easier to read and easier to write:

```
from steffentools import dict_to_ntuple

DEMO = dict_to_ntuple(DEMO_DICT)

# Display the contents of the namedtuple.
print(f"Result: {DEMO.result}")
print("Messages:")
for message in DEMO.message_list:
    print(f"  {message.id}: {message.msg}")
print("Errors:")
for error in DEMO.errors:
    print(f"  {error}")
print(f"Nest: type='{DEMO.nest.type}',"
      f"material='{DEMO.nest.material}'")
```

`dict_to_ntuple` will parse through the entire nested structure of the provided dictionary recursively and attempt to convert all elements into the `namedtuple` format. Any elements (such as lists or tuples) which are collections of sub-elements will be parsed, and `dict_to_ntuple` will attempt to convert those as well. Everything else will be returned as-is.

Some dictionary keys, such as integers, are impossible to convert. In these cases, the dictionary will be left as a dictionary, but `dict_to_ntuple` will attempt to convert all of the values stored in that dictionary. For example:

```
>>> from steffentools import dict_to_ntuple
>>> DEMO_DICT = {
...     1: "first element",
...     2: {"example": "success"},
... }
>>> DEMO = dict_to_ntuple(DEMO_DICT)
>>> print(DEMO[1])
first element
>>> print(DEMO[2].example)
success
```
