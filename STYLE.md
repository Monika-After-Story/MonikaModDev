# Coding Style

We don't have a strict style guideline, but here's a couple of conventions
we like to follow:

### Labels

Label names should be lowercase and separated with underscores (`monika_twitter`). 
If you use many labels for a related subprogram, prefix them with the name of 
your subprogram. Certain prefixes are reserved:

- `greeting` - used for regular greetings
- `i_greeting` - used for special interactive greetings
- `ch30` - used for key chapter 30 labels
- `monika` - used for nearly every monika topic
- `joke` - used for the jokes system
- `m_joke` - also used for the jokes sytem
- `mas_poem` - used for poemgame system
- `game` - used for most of the minigames
- `vv` - used for update-related material
- `v` - also used for update-related material

There may be more, so in general, be mindful of the labels you use. Try to be
as specific as possible to avoid overlap.

### Store

In Renpy, stores are like namespaces, except you can't have nested ones. We
recommend grouping related data, constants, and functions in stores to avoid
messing with the global namespace.

To create a store:
```python
init python in store_name:
    var1 = 1
    var2 = 2
    ...

# or
define store_name.var1 = 1
define store_name.var2 = 2
```

To access a store:
```python
store.store_name.var1 = 1

# or
python:
    import store.store_name as store_name
    store_name.var1 = 1
```

We use several different stores to group different data. when deciding to make
a new store, ensure that it is not already in use.

`persistent` is like a store, but its a special one that gets saved to disk.
**Only use this if you need to save data from multiple sessions** 
More on this later...

### Functions

If a function is very specific to a subprogram or flow, consider making it in 
a store and importing it when necessary. If a function can be generalized for
many use cases, then make it in a regular `init python` block (which makes it
global).

For documentation, either block comments (#) or doc strings (""") are fine. We
don't enforce a particular way of documenting functions, but noting what the
function does, its input and output vars, what it returns, and variables it
assumes would be a good start:

```python
def someKindOfFunction(var1, var2, var3=None):
    """
    This function does some kind of thing. Use with caution.

    IN:
        var1 - value of something
        var3 - like the most value of something
            (Default: None)

    OUT:
        var2 - contains modified reference to something

    RETURNS:
        a copy of var2

    ASSUMES:
        persistent.var4 
    """
```
For function names, either camelCase or lowercase_underscores are fine.

### Persistent

This store-like thing saves data to disk and is how renpy keeps track of data.
Because its already loaded with data from the stock game, **avoid using this
if you can**. (I.e: instead of using a persistent to check if an event has been
seen, use `renpy.seen_label` or `seen_event`. If you do need to use this, prefix
your variable names so we avoid collisions. Also make the persistent names pretty
descriptive, and use lowercase_underscores for naming.

### Constants

Define constants instead of literals when you're using them multiple times. 
Use UPPERCASE_UNDERSCORES for naming.

**An exception to this is literals used in screens**. If a screen is **not**
called with `nopredict`, then use literals when you can, as renpy optimizes 
screens with literals.

### Variables

Make these descriptive please. It doesn't need to be Java-like, just enough so
its somewhat easy to figure out what it is. Using abbreviations or acronyms is
fine. Use lowercase_underscores for naming.

### Comments

Please write comments. Even though python is readable as is, knowing the
high level reason why we are doing something or the high level effects of
doing something is helpful. 

### Line Length

Again, not really enforced, but keep them reasonable. I personally limit to 80
columns, but beyond that to probably 120 is fine. 
**The exception is Renpy code.** Renpy code cannot always be broken up into 
multiple lines.

### Assets

Any assets you use must be in the `mod_assets/` folder. If you have a ton of 
assets, group them into a subfolder.

### 3rd-party Packages

If you can do it without using an external package, then do it without the
external package. Exceptions must be discussed with the dev team. If whatever
library you want to add is more than a megabyte, it almost certainly will **not**
be allowed.
